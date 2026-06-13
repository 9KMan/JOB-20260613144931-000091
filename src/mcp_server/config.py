"""MCP Server configuration — loads from config.yaml and environment variables."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPServerSettings(BaseSettings):
    """Main MCP Server settings."""

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Settings
    internal_api_url: str = Field(
        default="https://internal-api.example.com",
        description="Base URL of the client's internal API",
    )
    internal_api_key: str = Field(
        default="***",
        description="API key for the internal API",
    )

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./mcp_server.db",
        description="Database connection URL (SQLite for PoC, PostgreSQL for prod)",
    )

    # Cache
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis URL (optional — in-memory dict used if not set)",
    )

    # LLM
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key for LLM calls",
    )

    # Auth
    mcp_api_key: str = Field(
        default="mcp_secret_key_change_in_production",
        description="API key for MCP client authentication",
    )

    # Observability
    log_level: str = Field(default="INFO", description="Logging level")


def load_config(config_path: Optional[str] = None) -> MCPServerSettings:
    """Load config from YAML file and environment variables.

    Environment variables override YAML values.
    """
    settings_dict: dict = {}

    if config_path and Path(config_path).exists():
        with open(config_path, encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f) or {}
            settings_dict.update(yaml_config)

    return MCPServerSettings(**settings_dict)
