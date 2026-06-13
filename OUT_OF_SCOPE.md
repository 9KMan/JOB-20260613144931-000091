# Out of Scope — PoC Boundaries

> ⚠️ **This is a Proof of Concept (PoC).** Many production features are explicitly excluded. Do not use this code in production without a thorough security and architecture review.

## Authentication & Authorization

| Feature | Status | Note |
|---------|--------|------|
| Production OAuth2/OIDC | **OUT** | Static API key only |
| Fine-grained RBAC | **OUT** | Single admin role |
| JWT token validation | **OUT** | Static credentials |
| Multi-tenancy | **OUT** | Single shared config |
| API key rotation | **OUT** | Manual restart required |

## Infrastructure

| Feature | Status | Note |
|---------|--------|------|
| Kubernetes | **OUT** | Docker Compose only |
| Production PostgreSQL | **OUT** | SQLite for PoC |
| Redis | **OUT** | In-memory dict cache |
| TLS/SSL | **OUT** | HTTP only |
| Database migrations | **OUT** | Schema init only |

## MCP Protocol Coverage (PoC)

| Feature | Status |
|---------|--------|
| `tools/list` | ✅ |
| `tools/call` (6 core tools) | ✅ |
| `resources/*` | ✗ |
| `prompts/*` | ✗ |
| `logging` | ✗ |

## Agent Capabilities (PoC)

| Feature | Status | Note |
|---------|--------|------|
| Query Understanding Agent | ✅ | Rule-based parser |
| Data Retrieval Agent | ✅ | Mock responses only |
| Response Synthesis Agent | ✅ | Template-based |
| Real internal API calls | ✗ | Mock data only |
| Real embeddings / RAG | ✗ | Schema only |

## Observability

| Feature | Status |
|---------|--------|
| Distributed tracing | ✗ |
| Prometheus metrics | ✗ |
| Circuit breakers | ✗ |
| Retry with backoff | ✗ |

## Production Checklist

Before using in production, address:

- [ ] Replace SQLite with PostgreSQL + pgvector
- [ ] Wire real internal API calls into `DataRetrievalAgent`
- [ ] Add TLS termination
- [ ] Add OAuth2/OIDC authentication
- [ ] Add Prometheus metrics endpoint
- [ ] Add retry with exponential backoff
- [ ] Add distributed tracing (OpenTelemetry)
- [ ] Replace in-memory cache with Redis
- [ ] Run security review of API credential storage
