from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(slots=True)
class ConnectorConfig:
    kind: str
    settings: dict[str, Any]


@dataclass(slots=True)
class AppConfig:
    connectors: list[ConnectorConfig] = field(default_factory=list)
    max_results_per_source: int = 5

    @classmethod
    def from_file(cls, path: str | Path) -> "AppConfig":
        content = Path(path).read_text(encoding="utf-8")
        raw = json.loads(content)
        max_results = int(raw.get("max_results_per_source", 5))
        connectors = []
        for kind, entries in raw.get("connectors", {}).items():
            for settings in entries or []:
                connectors.append(ConnectorConfig(kind=kind, settings=settings))
        return cls(connectors=connectors, max_results_per_source=max_results)


def group_connectors(connectors: Iterable[ConnectorConfig]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for connector in connectors:
        grouped.setdefault(connector.kind, []).append(connector.settings)
    return grouped
