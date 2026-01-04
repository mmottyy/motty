from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Iterable

import requests

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class ConfluenceConnector(Connector):
    base_url: str
    email: str
    api_token: str

    kind: str = "confluence"

    def _auth_header(self) -> dict[str, str]:
        token = base64.b64encode(f"{self.email}:{self.api_token}".encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {token}"}

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        url = f"{self.base_url.rstrip('/')}/rest/api/content/search"
        params = {"cql": f'text~"{query}"', "limit": max_results}
        response = requests.get(url, params=params, headers=self._auth_header(), timeout=20)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        for item in results[:max_results]:
            title = item.get("title", "")
            links = item.get("_links", {})
            webui = links.get("webui", "")
            url_full = f"{self.base_url.rstrip('/')}{webui}" if webui else self.base_url
            snippet = item.get("excerpt", "") or ""
            yield SearchResult(
                source="Confluence",
                title=title,
                url=url_full,
                snippet=str(snippet)[:240],
            )
