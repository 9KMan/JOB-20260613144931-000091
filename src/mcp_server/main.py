"""MCP Server — FastMCP-based server for natural-language data querying."""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

from mcp_server import __version__
from mcp_server.agents.data_retrieval import DataRetrievalAgent
from mcp_server.agents.query_understanding import understand_query
from mcp_server.agents.response_synthesis import synthesize_response
from mcp_server.cache import cache
from mcp_server.config import load_config
from mcp_server.database import init_db, QueryLog, Collection
from sqlalchemy import select

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("mcp_server")

# ---------------------------------------------------------------------------
# Config + agents
# ---------------------------------------------------------------------------

config = load_config()
retrieval_agent = DataRetrievalAgent(
    api_url=config.internal_api_url,
    api_key=config.internal_api_key,
)

# ---------------------------------------------------------------------------
# FastMCP instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="MCP Server",
    description="Natural-language data querying via MCP protocol",
    version=__version__,
)


# ---------------------------------------------------------------------------
# MCP Tool: query_dataset
# ---------------------------------------------------------------------------

@mcp.tool()
async def query_dataset(
    question: str,
    context: dict | None = None,
    options: dict | None = None,
) -> dict[str, Any]:
    """Execute a natural-language query against the dataset.

    Args:
        question: Natural language question about the data.
        context: Optional context (filters, date range).
        options: maxResults, includeRawData, responseFormat.

    Returns:
        Structured results with natural-language answer and citations.
    """
    start = time.time()
    opts = options or {}

    # Check cache
    cache_key = f"query:{question}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    # Query understanding
    query_plan = await understand_query(question)
    collection = query_plan.get("collection", "dataset")
    output_format = query_plan.get("output_format", opts.get("responseFormat", "detailed"))

    # Data retrieval
    data = await retrieval_agent.retrieve(
        collection=collection,
        query=question,
        limit=opts.get("maxResults", 50),
    )

    # Response synthesis
    response_text = await synthesize_response(
        question=question,
        data=data,
        output_format=output_format,
    )

    result = {
        "content": [
            {"type": "text", "text": response_text}
        ],
        "metrics": {
            "executionTimeMs": int((time.time() - start) * 1000),
        },
    }

    # Cache result (5 min TTL)
    cache.set(cache_key, result, ttl_seconds=300)

    return result


# ---------------------------------------------------------------------------
# MCP Tool: aggregate_data
# ---------------------------------------------------------------------------

@mcp.tool()
async def aggregate_data(
    question: str,
    metrics: list[dict],
    group_by: list[str] | None = None,
    filters: list | None = None,
) -> dict[str, Any]:
    """Perform aggregations (count, sum, avg, min, max) on the dataset.

    Args:
        question: Aggregation request in natural language.
        metrics: List of metric definitions with field, operation, alias.
        group_by: Fields to group results by.
        filters: Optional filter conditions.

    Returns:
        Aggregation results.
    """
    start = time.time()

    # Query understanding
    query_plan = await understand_query(question)
    collection = query_plan.get("collection", "dataset")

    # Aggregation
    data = await retrieval_agent.aggregate(
        collection=collection,
        group_by=group_by or [],
        metrics=metrics,
    )

    response_text = await synthesize_response(
        question=question,
        data=data,
        output_format="table",
    )

    return {
        "content": [{"type": "text", "text": response_text}],
        "metrics": {"executionTimeMs": int((time.time() - start) * 1000)},
    }


# ---------------------------------------------------------------------------
# MCP Tool: search_similar
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_similar(
    description: str,
    collection: str,
    limit: int = 10,
    threshold: float = 0.7,
) -> dict[str, Any]:
    """Find records semantically similar to a description using vector similarity.

    Args:
        description: Natural language description.
        collection: Target data collection.
        limit: Max results to return.
        threshold: Minimum similarity score (0-1).

    Returns:
        Similar records with similarity scores.
    """
    start = time.time()
    data = await retrieval_agent.search_similar(
        collection=collection,
        description=description,
        limit=limit,
    )

    response_text = await synthesize_response(
        question=f"Find items similar to: {description}",
        data=data,
        output_format="detailed",
    )

    return {
        "content": [{"type": "text", "text": response_text}],
        "metrics": {"executionTimeMs": int((time.time() - start) * 1000)},
    }


# ---------------------------------------------------------------------------
# MCP Tool: list_collections
# ---------------------------------------------------------------------------

@mcp.tool()
async def list_collections(category: str | None = None) -> dict[str, Any]:
    """List all available data collections (tables, API endpoints).

    Args:
        category: Optional filter by category.

    Returns:
        List of available collections.
    """
    # MOCK collections for PoC
    all_collections = [
        {"name": "transactions", "description": "Financial transaction records", "category": "finance"},
        {"name": "customers", "description": "Customer records", "category": "crm"},
        {"name": "products", "description": "Product catalog", "category": "inventory"},
        {"name": "logs", "description": "System log entries", "category": "operations"},
    ]

    filtered = all_collections
    if category:
        filtered = [c for c in filtered if c.get("category") == category]

    text = "Available collections:\n" + "\n".join(
        f"  • {c['name']}: {c['description']}" for c in filtered
    )

    return {"content": [{"type": "text", "text": text}]}


# ---------------------------------------------------------------------------
# MCP Tool: describe_collection
# ---------------------------------------------------------------------------

@mcp.tool()
async def describe_collection(
    collection: str,
    include_samples: bool = False,
) -> dict[str, Any]:
    """Get detailed schema information for a specific collection.

    Args:
        collection: Name of the collection.
        include_samples: Include sample values.

    Returns:
        Collection schema and optionally sample records.
    """
    schemas = {
        "transactions": {
            "name": "transactions",
            "description": "Financial transaction records",
            "fields": [
                {"name": "id", "type": "string", "description": "Unique transaction ID"},
                {"name": "amount", "type": "number", "description": "Transaction amount"},
                {"name": "currency", "type": "string", "description": "ISO 4217 currency code"},
                {"name": "status", "type": "string", "description": "pending | completed | failed"},
                {"name": "created_at", "type": "datetime", "description": "Timestamp"},
            ],
        },
        "customers": {
            "name": "customers",
            "description": "Customer records",
            "fields": [
                {"name": "id", "type": "string", "description": "Unique customer ID"},
                {"name": "name", "type": "string", "description": "Full name"},
                {"name": "email", "type": "string", "description": "Email address"},
                {"name": "tier", "type": "string", "description": "Customer tier: basic | premium | enterprise"},
            ],
        },
        "products": {
            "name": "products",
            "description": "Product catalog",
            "fields": [
                {"name": "id", "type": "string", "description": "Unique product ID"},
                {"name": "name", "type": "string", "description": "Product name"},
                {"name": "price", "type": "number", "description": "Price in USD"},
                {"name": "category", "type": "string", "description": "Product category"},
            ],
        },
    }

    if collection not in schemas:
        return {
            "content": [{"type": "text", "text": f"Collection '{collection}' not found."}],
        }

    schema = schemas[collection]
    lines = [f"Collection: {schema['name']}", f"Description: {schema['description']}", "", "Fields:"]
    for field in schema["fields"]:
        lines.append(f"  • {field['name']} ({field['type']}): {field['description']}")

    return {"content": [{"type": "text", "text": "\n".join(lines)}]}


# ---------------------------------------------------------------------------
# MCP Tool: export_data
# ---------------------------------------------------------------------------

@mcp.tool()
async def export_data(
    query: str,
    format: str = "csv",
    filename: str = "export",
) -> dict[str, Any]:
    """Export query results in specified format.

    Args:
        query: Description of data to export.
        format: csv | json | xlsx.
        filename: Output filename (without extension).

    Returns:
        Download link or file content.
    """
    import base64

    # Generate mock export
    if format == "json":
        content = json.dumps({"query": query, "data": []}, indent=2)
        ext = "json"
    else:
        content = f"id,name,status\n001,Sample Item,active\n"
        ext = "csv"

    b64 = base64.b64encode(content.encode()).decode()

    return {
        "content": [
            {"type": "text", "text": f"Export ready: {filename}.{ext}"},
            {"type": "resource", "data": b64, "mimeType": f"application/{ext}"},
        ],
    }


# ---------------------------------------------------------------------------
# FastAPI app (supplementary REST endpoints)
# ---------------------------------------------------------------------------

app = FastAPI(title="MCP Server REST API", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    """Initialize database and log startup."""
    await init_db()
    log.info(f"MCP Server v{__version__} starting — log_level={config.log_level}")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": __version__}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def run() -> None:
    """Run the MCP server."""
    import asyncio

    async def _main() -> None:
        await init_db()
        log.info(f"Starting MCP Server v{__version__}")
        # Run as stdio MCP server
        await mcp.run()

    asyncio.run(_main())


if __name__ == "__main__":
    run()
