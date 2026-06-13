"""Async SQLAlchemy database session and models."""
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator

from sqlalchemy import JSON, Column, DateTime, String, Text, Boolean, Index
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./mcp_server.db"


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class QueryLog(Base):
    """Audit log for all MCP queries."""

    __tablename__ = "query_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), nullable=True, index=True)
    question = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)
    tools_used = Column(JSON, nullable=True)
    result_summary = Column(Text, nullable=True)
    execution_time_ms = Column(String(50), nullable=True)
    status = Column(String(50), default="success")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (Index("idx_query_logs_created", "created_at"),)


class Collection(Base):
    """Registry of available data collections (tables/endpoints)."""

    __tablename__ = "collections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    schema_definition = Column(JSON, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    is_vectorized = Column(Boolean, default=False)
    api_endpoint = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class APICredential(Base):
    """Encrypted API credentials for internal services."""

    __tablename__ = "api_credentials"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    endpoint = Column(String(500), nullable=False)
    auth_type = Column(String(50), nullable=True)
    encrypted_headers = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Engine + session factory
# ---------------------------------------------------------------------------

_engine = create_async_engine(DATABASE_URL, echo=False)
_async_session_factory = async_sessionmaker(bind=_engine, expire_on_commit=False)


async def init_db() -> None:
    """Create all tables. Call once on startup."""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI / MCP handlers."""
    async with _async_session_factory() as session:
        yield session


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for manual session handling."""
    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
