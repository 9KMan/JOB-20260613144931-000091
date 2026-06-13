"""Tests for MCP Server tools, cache, and agents."""
import pytest
import time

from mcp_server.cache import Cache
from mcp_server.agents.query_understanding import understand_query
from mcp_server.agents.response_synthesis import synthesize_response


class TestCache:
    def test_get_set(self, cache: Cache) -> None:
        cache.set("key1", "value1", ttl_seconds=60)
        assert cache.get("key1") == "value1"

    def test_expired_key(self, cache: Cache) -> None:
        cache.set("key2", "value2", ttl_seconds=1)
        time.sleep(1.1)
        assert cache.get("key2") is None

    def test_delete(self, cache: Cache) -> None:
        cache.set("key3", "value3")
        cache.delete("key3")
        assert cache.get("key3") is None

    def test_clear(self, cache: Cache) -> None:
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None


class TestQueryUnderstanding:
    @pytest.mark.asyncio
    async def test_aggregation_intent(self) -> None:
        result = await understand_query("How many transactions were made?")
        assert result["intent"] == "aggregation"

    @pytest.mark.asyncio
    async def test_search_similar_intent(self) -> None:
        result = await understand_query("Find items similar to product X")
        assert result["intent"] == "search_similar"

    @pytest.mark.asyncio
    async def test_lookup_intent(self) -> None:
        result = await understand_query("List all customers")
        assert result["intent"] == "lookup"


class TestResponseSynthesis:
    @pytest.mark.asyncio
    async def test_json_format(self) -> None:
        data = {"collection": "test", "records": [{"id": "1", "name": "Item"}], "total": 1}
        result = await synthesize_response("test question", data, output_format="json")
        assert "Item" in result
        assert "test question" in result

    @pytest.mark.asyncio
    async def test_empty_records(self) -> None:
        data = {"collection": "test", "records": [], "total": 0}
        result = await synthesize_response("test", data, output_format="detailed")
        assert "No records found" in result


class TestIntegration:
    @pytest.mark.asyncio
    async def test_end_to_end_query(self) -> None:
        """Smoke test: understand a query and synthesize a response."""
        question = "How many orders were placed this month?"
        plan = await understand_query(question)
        assert plan["intent"] == "aggregation"

        data = {"collection": "orders", "records": [{"id": "1"}], "total": 1}
        response = await synthesize_response(question, data)
        assert "orders" in response.lower()
