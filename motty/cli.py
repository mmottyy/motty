from __future__ import annotations

import argparse
from typing import Iterable

from motty.config import AppConfig, group_connectors
from motty.connectors.confluence import ConfluenceConnector
from motty.connectors.jira import JiraConnector
from motty.connectors.mcp import McpConnector
from motty.connectors.nas import NasConnector
from motty.connectors.sharepoint import SharePointConnector
from motty.engine import ChatEngine


def build_connectors(config: AppConfig) -> Iterable[object]:
    grouped = group_connectors(config.connectors)
    for settings in grouped.get("jira", []):
        yield JiraConnector(**settings)
    for settings in grouped.get("confluence", []):
        yield ConfluenceConnector(**settings)
    for settings in grouped.get("sharepoint", []):
        yield SharePointConnector(**settings)
    for settings in grouped.get("nas", []):
        yield NasConnector(**settings)
    for settings in grouped.get("mcp", []):
        yield McpConnector(**settings)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Motty multi-source chatbot search")
    parser.add_argument("question", help="Natural language query")
    parser.add_argument("--config", default="config.json", help="Path to config JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AppConfig.from_file(args.config)
    engine = ChatEngine(build_connectors(config), max_results_per_source=config.max_results_per_source)
    response = engine.query(args.question)
    print(response.render())


if __name__ == "__main__":
    main()
