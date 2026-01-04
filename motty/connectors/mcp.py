from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class McpConnector(Connector):
    base_url: str
    api_key: str | None = None

    kind: str = "mcp"

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        url = f"{self.base_url.rstrip('/')}/query"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(url, json={"query": query, "limit": max_results}, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        for item in data.get("results", [])[:max_results]:
            yield SearchResult(
                source=item.get("source", "MCP"),
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet", "")[:240],
            )
