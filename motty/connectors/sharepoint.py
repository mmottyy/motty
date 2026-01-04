from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class SharePointConnector(Connector):
    tenant_id: str
    client_id: str
    client_secret: str

    kind: str = "sharepoint"

    def _token(self) -> str:
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
        response = requests.post(token_url, data=data, timeout=20)
        response.raise_for_status()
        return response.json()["access_token"]

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        token = self._token()
        url = "https://graph.microsoft.com/v1.0/search/query"
        payload = {
            "requests": [
                {
                    "entityTypes": ["driveItem", "listItem"],
                    "query": {"queryString": query},
                    "from": 0,
                    "size": max_results,
                }
            ]
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        hits = (
            data.get("value", [{}])[0]
            .get("hitsContainers", [{}])[0]
            .get("hits", [])
        )
        for hit in hits[:max_results]:
            resource = hit.get("resource", {})
            title = resource.get("name") or resource.get("title") or ""
            url_full = resource.get("webUrl", "")
            snippet = hit.get("summary", "") or ""
            yield SearchResult(
                source="SharePoint",
                title=title,
                url=url_full,
                snippet=str(snippet)[:240],
            )
