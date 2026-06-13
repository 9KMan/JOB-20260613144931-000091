"""Pytest configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Ensure src is on the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server.cache import Cache


@pytest.fixture
def cache() -> Cache:
    """Fresh in-memory cache for each test."""
    c = Cache()
    yield c
    c.clear()
