# MCP Server

> Natural-language data querying via Model Context Protocol (MCP)

**Built by:** KMan | AI-Augmented Engineering Factory

## What This Is

An MCP Server that wraps a client's internal API, enabling AI agents to answer natural-language questions against the connected dataset. Users query structured data using conversational language — no SQL, no API knowledge required.

## Architecture

```
MCP Client (Claude Desktop, custom clients)
    │
    │ JSON-RPC 2.0 over stdio
    ▼
┌─────────────────────────────────────────────────┐
│  MCP Server (FastMCP)                           │
│  ├── query_dataset — NL query against dataset    │
│  ├── aggregate_data — count/sum/avg/min/max     │
│  ├── search_similar — vector similarity search   │
│  ├── list_collections — available data sources   │
│  ├── describe_collection — schema inspection      │
│  └── export_data — CSV/JSON export               │
│                                                 │
│  Agents: Query Understanding → Retrieval → NL    │
└─────────────────────────────────────────────────┘
    │
    │ httpx (mock in PoC, real API in production)
    ▼
Client Internal API
```

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/9KMan/JOB-20260613144931-000091.git
cd JOB-20260613144931-000091
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Configure (edit config.yaml)
cp config.yaml config.local.yaml

# 3. Run
python -m mcp_server.main

# 4. Test
curl http://localhost:8000/health

# 5. Run tests
pytest tests/ -v
```

## Docker

```bash
docker compose up --build
curl http://localhost:8000/health
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.11+ |
| MCP Framework | FastMCP (mcp Python SDK) |
| Web | FastAPI |
| Database | SQLite (PoC) / PostgreSQL (prod) |
| HTTP Client | httpx |
| Config | pydantic-settings |

## Project Structure

```
src/mcp_server/
├── __init__.py          # Package entry
├── __version__.py       # Version
├── config.py            # Settings management
├── database.py          # ORM models (SQLAlchemy async)
├── cache.py             # In-memory TTL cache
├── main.py              # FastMCP server + REST endpoints
└── agents/
    ├── query_understanding.py   # Intent classification
    ├── data_retrieval.py        # API client (mock in PoC)
    └── response_synthesis.py    # NL response generation
```

## Configuration

Copy `config.yaml` to `config.local.yaml` and set:

| Variable | Description | Default |
|----------|-------------|---------|
| `internal_api_url` | Internal API base URL | `https://internal-api.example.com` |
| `internal_api_key` | Internal API key | `***` |
| `database_url` | SQLite or PostgreSQL URL | `sqlite+aiosqlite://...` |
| `anthropic_api_key` | Anthropic API key | (optional for PoC) |
| `mcp_api_key` | MCP authentication | `mcp_secret...` |

## MCP Tools

| Tool | Description |
|------|-------------|
| `query_dataset` | Execute natural-language query against dataset |
| `aggregate_data` | Perform count/sum/avg/min/max aggregations |
| `search_similar` | Vector similarity search (pgvector in prod) |
| `list_collections` | List available data collections |
| `describe_collection` | Show schema for a collection |
| `export_data` | Export results as CSV/JSON |

## Business Problem Solved

Domain experts typically need engineering support to query internal data. This MCP Server lets them ask questions in plain English — "What were our Q3 sales by region?" — and get structured answers immediately, without writing SQL or understanding the underlying API schema.

## Limitations

⚠️ This is a **PoC build**. See [OUT_OF_SCOPE.md](OUT_OF_SCOPE.md) for what's explicitly excluded.

- Only mock data in PoC (no real API calls)
- SQLite database (not production PostgreSQL)
- Static API key auth (no OAuth2)
- Rule-based query understanding (no LLM in PoC)
- No multi-tenancy

## Deploy to Production

1. Replace `DataRetrievalAgent` with real httpx calls to your internal API
2. Switch `database_url` from SQLite to PostgreSQL + pgvector
3. Add TLS termination in front of the server
4. Replace static API key auth with OAuth2/OIDC
5. Review `OUT_OF_SCOPE.md` for full checklist
