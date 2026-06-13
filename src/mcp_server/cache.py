"""In-memory cache — Redis-compatible interface, no external deps."""
from __future__ import annotations

import time
from typing import Any, Optional


class Cache:
    """Simple in-memory TTL cache (Redis shape, no Redis required for PoC)."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}  # key → (value, expiry_timestamp)

    def get(self, key: str) -> Optional[Any]:
        """Get a value if it exists and hasn't expired."""
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if expiry < time.time():
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Set a value with a TTL (default 5 minutes)."""
        self._store[key] = (value, time.time() + ttl_seconds)

    def delete(self, key: str) -> None:
        """Delete a key."""
        self._store.pop(key, None)

    def clear(self) -> None:
        """Clear all entries."""
        self._store.clear()

    async def ping(self) -> bool:
        """Always returns True — compatibility with Redis client interface."""
        return True


# Global cache instance
cache = Cache()
