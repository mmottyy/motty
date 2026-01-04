from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class SearchResult:
    source: str
    title: str
    url: str
    snippet: str


class Connector:
    kind: str = "base"

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        raise NotImplementedError
