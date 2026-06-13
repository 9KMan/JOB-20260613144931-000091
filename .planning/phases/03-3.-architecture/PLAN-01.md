# Phase 03: Architecture

## Phase Goal
Implement the MCP protocol handler, agent pipeline, and data flow components.

## Preconditions
- Phase 2 complete (FastAPI, MCP SDK, config, DB session working)

## Tasks
- [ ] Implement `src/mcp_server/protocol/handler.py` — JSON-RPC 2.0 request routing
- [ ] Implement `src/mcp_server/protocol/errors.py` — MCPError classes with codes
- [ ] Build `src/mcp_server/tools/registry.py` — dynamic tool registration and invocation
- [ ] Create `src/mcp_server/agents/query_understanding.py` — intent classification, entity extraction
- [ ] Create `src/mcp_server/agents/data_retrieval.py` — API client with retry logic, mock responses
- [ ] Create `src/mcp_server/agents/response_synthesis.py` — NL generation from structured results
- [ ] Create `src/mcp_server/middleware.py` — request logging middleware
- [ ] Wire agents into tool handlers; verify end-to-end request flow

## Deliverables
- `src/mcp_server/protocol/handler.py`
- `src/mcp_server/protocol/errors.py`
- `src/mcp_server/tools/registry.py`
- `src/mcp_server/agents/query_understanding.py`
- `src/mcp_server/agents/data_retrieval.py`
- `src/mcp_server/agents/response_synthesis.py`
- `src/mcp_server/middleware.py`

## Verification
- [ ] MCP initialize request returns capabilities object
- [ ] tools/list returns all 6 tool definitions
- [ ] agents produce output from mock inputs without exceptions
