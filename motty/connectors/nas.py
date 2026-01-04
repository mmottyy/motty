from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from motty.connectors.base import Connector, SearchResult


@dataclass(slots=True)
class NasConnector(Connector):
    root_path: str

    kind: str = "nas"

    def search(self, query: str, max_results: int) -> Iterable[SearchResult]:
        root = Path(self.root_path)
        if not root.exists():
            return []
        results = []
        lowered = query.lower()
        for path in root.rglob("*"):
            if len(results) >= max_results:
                break
            if not path.is_file():
                continue
            if lowered in path.name.lower():
                results.append(
                    SearchResult(
                        source="NAS",
                        title=path.name,
                        url=str(path.resolve()),
                        snippet="matched filename",
                    )
                )
                continue
            if path.stat().st_size > 2_000_000:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if lowered in content.lower():
                snippet = content.strip().replace("\n", " ")[:240]
                results.append(
                    SearchResult(
                        source="NAS",
                        title=path.name,
                        url=str(path.resolve()),
                        snippet=snippet,
                    )
                )
        return results
