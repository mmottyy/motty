from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Iterable

import requests

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class JiraConnector(Connector):
    base_url: str
    email: str
    api_token: str

    kind: str = "jira"

    def _auth_header(self) -> dict[str, str]:
        token = base64.b64encode(f"{self.email}:{self.api_token}".encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {token}"}

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        url = f"{self.base_url.rstrip('/')}/rest/api/3/search"
        params = {
            "jql": f'text ~ "{query}"',
            "maxResults": max_results,
            "fields": "summary,description",
        }
        response = requests.get(url, params=params, headers=self._auth_header(), timeout=20)
        response.raise_for_status()
        data = response.json()
        issues = data.get("issues", [])
        for issue in issues[:max_results]:
            key = issue.get("key", "")
            fields = issue.get("fields", {})
            summary = fields.get("summary", "")
            description = fields.get("description")
            snippet = ""
            if isinstance(description, dict):
                snippet = description.get("content", "")
            yield SearchResult(
                source="JIRA",
                title=f"{key} {summary}".strip(),
                url=f"{self.base_url.rstrip('/')}/browse/{key}" if key else self.base_url,
                snippet=str(snippet)[:240],
            )
