# Phase 05: Project Structure

## Phase Goal
Finalize the package layout, CLI entry point, configuration files, and testing setup.

## Preconditions
- Phase 1–4 complete

## Tasks
- [ ] Create `src/mcp_server/__init__.py` — public API exports, version
- [ ] Create `src/mcp_server/__main__.py` — `python -m mcp_server` entry point
- [ ] Create `src/mcp_server/cli.py` — argument parsing for config file path
- [ ] Create `config.yaml` — template with all required env vars documented
- [ ] Create `.env.example` — copy of required env vars
- [ ] Set up `tests/` with `conftest.py` — fixtures for DB, cache, mock agents
- [ ] Add `tests/test_tools.py` — smoke test for each tool handler
- [ ] Add `tests/test_protocol.py` — test MCP request/response roundtrips
- [ ] Create `Dockerfile` and `docker-compose.yml` — full stack with SQLite (no postgres for PoC)
- [ ] Update `README.md` — project overview, quickstart (5 steps), architecture summary

## Deliverables
- `src/mcp_server/__init__.py`
- `src/mcp_server/__main__.py`
- `src/mcp_server/cli.py`
- `config.yaml`
- `.env.example`
- `tests/conftest.py`
- `tests/test_tools.py`
- `tests/test_protocol.py`
- `Dockerfile`
- `docker-compose.yml`
- `README.md`

## Verification
- [ ] `python -m mcp_server --help` works
- [ ] `pytest tests/ -v` passes with 0 failures
- [ ] `docker compose build` succeeds
- [ ] `docker compose up -d && sleep 3 && curl http://localhost:8000/health` returns 200
- [ ] README quickstart completes in 5 steps or fewer
