from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class ChatResponse:
    query: str
    results: list[SearchResult]

    def render(self) -> str:
        if not self.results:
            return f"No results found for '{self.query}'."
        lines = [f"Results for '{self.query}':"]
        for result in self.results:
            lines.append(f"- [{result.source}] {result.title}: {result.url}")
            if result.snippet:
                lines.append(f"  {result.snippet}")
        return "\n".join(lines)


class ChatEngine:
    def __init__(self, connectors: Iterable[Connector], max_results_per_source: int = 5) -> None:
        self.connectors = list(connectors)
        self.max_results_per_source = max_results_per_source

    def query(self, question: str) -> ChatResponse:
        results: list[SearchResult] = []
        for connector in self.connectors:
            try:
                results.extend(list(connector.search(question, self.max_results_per_source)))
            except Exception as exc:
                results.append(
                    SearchResult(
                        source=connector.kind,
                        title="Error",
                        url="",
                        snippet=f"{connector.kind} connector failed: {exc}",
                    )
                )
        return ChatResponse(query=question, results=results)
