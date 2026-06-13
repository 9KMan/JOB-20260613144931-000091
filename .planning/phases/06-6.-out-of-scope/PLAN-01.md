# Phase 06: Out of Scope — PoC Boundaries

## Phase Goal
Document what the MCP Server PoC explicitly does NOT build, so expectations are clear.

## Preconditions
- SPEC.md reviewed and architecture agreed
- Phase 1–5 complete or in progress

## Deliverables
- `OUT_OF_SCOPE.md` — Full boundary document
- `README.md` updated with PoC limitations banner

## Out of Scope

### Authentication & Authorization
- Production OAuth2/OIDC — PoC uses static API key in config only
- Fine-grained RBAC — single admin role only
- JWT token validation — static credentials only
- Multi-tenancy — single shared configuration

### Infrastructure
- Kubernetes deployment — Docker Compose only
- Production PostgreSQL — SQLite for PoC
- Redis caching — in-memory dict for PoC
- TLS/SSL — HTTP only in PoC

### MCP Protocol Coverage (PoC)
- tools/list ✓
- tools/call (6 core tools) ✓
- resources/* ✗
- prompts/* ✗
- logging ✗

### Agent Capabilities (PoC)
- Query Understanding Agent ✓ (mock LLM)
- Data Retrieval Agent ✓ (mock API client)
- Response Synthesis Agent ✓ (mock LLM)
- Real internal API calls ✗ (mock responses only)
- Real embeddings/RAG ✗ (vector store schema only)

### Observability
- Distributed tracing ✗
- Prometheus metrics ✗
- Circuit breakers ✗
- Retry with backoff ✗

## Verification
- [ ] OUT_OF_SCOPE.md exists with all items documented
- [ ] README has PoC banner and link to OUT_OF_SCOPE.md
- [ ] No production secrets in codebase
- [ ] Mock components clearly labeled as MOCK in code comments
