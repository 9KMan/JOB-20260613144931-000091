# Phase 02: Technical Stack

## Phase Goal
Set up the Python project with FastAPI, MCP SDK, async PostgreSQL (via SQLite for PoC), and configuration management.

## Preconditions
- Phase 1 complete (pyproject.toml, requirements.txt exist)
- Python 3.11+ available

## Tasks
- [ ] Configure pydantic-settings for environment variable config loading
- [ ] Create `src/mcp_server/config.py` — loads from config.yaml and env vars
- [ ] Create `src/mcp_server/database.py` — async SQLAlchemy session, SQLite for PoC
- [ ] Create `src/mcp_server/cache.py` — in-memory dict cache (Redis shape, no deps)
- [ ] Integrate `mcp.server` SDK; create a minimal MCP server instance
- [ ] Create `src/mcp_server/main.py` — FastAPI app with lifespan events, /health endpoint
- [ ] Create `alembic.ini` and `alembic/` directory for future migrations
- [ ] Add structured logging (Python stdlib logging, JSON format)

## Deliverables
- `src/mcp_server/config.py`
- `src/mcp_server/database.py`
- `src/mcp_server/cache.py`
- `src/mcp_server/main.py`
- `alembic.ini`

## Verification
- [ ] `python -m mcp_server` starts without import errors
- [ ] `/health` returns 200
- [ ] Logs appear in stdout on startup
