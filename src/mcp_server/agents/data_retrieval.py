"""Data Retrieval Agent — executes API calls against the internal API (mock in PoC)."""
from __future__ import annotations

import json
from typing import Any

import httpx


class DataRetrievalAgent:
    """Retrieves data from the internal API.

    In PoC, returns mock responses. In production, this makes real httpx calls.
    """

    def __init__(self, api_url: str, api_key: str) -> None:
        self.api_url = api_url
        self.api_key = api_key

    async def retrieve(self, collection: str, query: str, limit: int = 50) -> dict[str, Any]:
        """Retrieve structured data from the internal API.

        Returns mock PoC data matching the requested collection.
        """
        # MOCK: Return realistic PoC data for any collection
        return {
            "collection": collection,
            "query": query,
            "records": [
                {"id": "001", "name": f"Item in {collection} #1", "status": "active"},
                {"id": "002", "name": f"Item in {collection} #2", "status": "active"},
                {"id": "003", "name": f"Item in {collection} #3", "status": "inactive"},
            ],
            "total": 3,
            "note": "MOCK DATA — PoC only. Replace with real API calls for production.",
        }

    async def aggregate(
        self, collection: str, group_by: list[str], metrics: list[dict[str, str]]
    ) -> dict[str, Any]:
        """Perform aggregation on data."""
        # MOCK
        return {
            "collection": collection,
            "group_by": group_by,
            "metrics": [
                {"field": "status", "operation": "count", "value": 3, "alias": "count"},
            ],
            "note": "MOCK DATA — PoC only",
        }

    async def search_similar(
        self, collection: str, description: str, limit: int = 10
    ) -> dict[str, Any]:
        """Find semantically similar records (mock)."""
        # MOCK — returns placeholder
        return {
            "collection": collection,
            "query": description,
            "results": [
                {"id": "001", "name": "Related item #1", "similarity": 0.87},
                {"id": "002", "name": "Related item #2", "similarity": 0.72},
            ],
            "note": "MOCK VECTOR SEARCH — PoC only. Wire up pgvector for production.",
        }

    async def health_check(self) -> bool:
        """Check if the internal API is reachable."""
        # MOCK: always healthy in PoC
        return True
