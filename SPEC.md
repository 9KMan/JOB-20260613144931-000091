# MCP Server for Natural-Language Data Querying

## Project Specification

## 1. Project Overview

### 1.1 Purpose

This project delivers a production-grade MCP (Model Context Protocol) Server that wraps a client's internal API, enabling AI agents to answer natural-language questions against the client's dataset. Users can query structured and unstructured data using conversational language without requiring knowledge of underlying database schemas, API endpoints, or query languages.

### 1.2 Problem Statement

Clients with internal APIs face the following challenges:
- Domain experts cannot self-serve data queries without engineering support
- Internal APIs expose implementation details that are opaque to non-technical users
- Natural-language access to data requires custom integrations that are expensive to maintain
- Existing query interfaces require training and often produce errors in complex queries

### 1.3 Solution Scope

The MCP Server provides:
- Standardized MCP protocol implementation for tool discovery and invocation
- AI agents that translate natural-language queries into API calls
- Retrieval-Augmented Generation (RAG) for context-aware answering
- Secure credential management and access control
- Observability and audit logging for compliance

### 1.4 Target Users

| User Type | Interaction Mode |
|-----------|------------------|
| Business Analysts | Direct NL queries via MCP client applications |
| Data Science Teams | Automated pipelines using MCP tools |
| Customer Support | Contextual data retrieval during conversations |
| Internal Applications | MCP client integration for embedded analytics |

---

## 2. Architecture

### 2.1 High-Level Architecture

```
MCP Client Applications (Claude Desktop, custom clients)
    │
    │ MCP Protocol (JSON-RPC 2.0 over stdio/HTTP SSE)
    ▼
┌──────────────────────────────────────────────────────────────┐
│  MCP Server                                                │
│  ├── MCP Protocol Handler (tool registry, resources,       │
│  │   prompts, request routing)                              │
│  ├── Query Understanding Agent                              │
│  │   (intent classification, entity extraction)            │
│  ├── Data Retrieval Agent                                   │
│  │   (RAG pipeline, API orchestration)                     │
│  └── Response Synthesis Agent                              │
│      (NL generation, citations)                             │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Client Internal Systems (PostgreSQL, Internal REST API, Vector Store)
```

### 2.2 Component Design

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| Protocol Handler | Parse MCP JSON-RPC messages, route requests | Python asyncio |
| Tool Registry | Maintain tool definitions, handle tool calls | In-memory + database |
| Query Understanding Agent | Parse NL input, extract intent and parameters | Claude/GPT via httpx |
| Data Retrieval Agent | Execute API calls, fetch relevant data | httpx + retry logic |
| Response Synthesis Agent | Generate natural-language answers | Claude/GPT via httpx |
| Vector Store | Store and search embeddings | PostgreSQL pgvector |
| Cache Layer | Cache frequent queries | Redis |

### 2.3 Data Flow

1. MCP Client sends JSON-RPC request
2. Protocol Handler receives and routes
3. Query Understanding Agent: classify intent, extract entities
4. Tool Execution: call appropriate tools via API client
5. RAG Pipeline: embed query, retrieve relevant context
6. Response Synthesis: generate NL answer with citations
7. MCP Protocol Handler returns JSON-RPC response

### 2.4 Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Runtime | Python | 3.11+ |
| Web Framework | FastAPI | 0.104+ |
| MCP SDK | mcp Python SDK | 0.3+ |
| Database | PostgreSQL | 15+ |
| Vector Extension | pgvector | 0.5+ |
| Cache | Redis | 7+ |
| Container | Docker | 24+ |
| HTTP Client | httpx | 0.25+ |
| LLM Client | anthropic | latest |

---

## 3. MCP Protocol Implementation

### 3.1 Server Capabilities

```json
{
  "capabilities": {
    "tools": { "listChanged": true },
    "resources": { "subscribe": true, "listChanged": true },
    "prompts": { "listChanged": true },
    "logging": {}
  }
}
```

### 3.2 Tool Definitions

#### query_dataset
Executes a natural-language query against the dataset. Returns structured results with citations.
```json
{
  "name": "query_dataset",
  "description": "Execute a natural-language query against the dataset. Returns structured results with citations.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "question": { "type": "string", "description": "Natural language question about the data" },
      "context": {
        "type": "object",
        "properties": {
          "filters": { "type": "object" },
          "dateRange": {
            "type": "object",
            "properties": {
              "start": { "type": "string", "format": "date" },
              "end": { "type": "string", "format": "date" }
            }
          }
        }
      },
      "options": {
        "type": "object",
        "properties": {
          "maxResults": { "type": "integer", "default": 50 },
          "includeRawData": { "type": "boolean", "default": false },
          "responseFormat": { "type": "string", "enum": ["concise", "detailed", "table", "json"] }
        }
      }
    },
    "required": ["question"]
  }
}
```

#### aggregate_data
Perform aggregations (count, sum, average, min, max) on the dataset.
```json
{
  "name": "aggregate_data",
  "description": "Perform aggregations on the dataset based on natural-language specifications.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "question": { "type": "string" },
      "groupBy": { "type": "array", "items": { "type": "string" } },
      "metrics": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "field": { "type": "string" },
            "operation": { "type": "string", "enum": ["count", "sum", "avg", "min", "max", "distinct"] },
            "alias": { "type": "string" }
          }
        }
      },
      "filters": { "type": "array" }
    },
    "required": ["question", "metrics"]
  }
}
```

#### search_similar
Find records semantically similar to a description using vector similarity search.
```json
{
  "name": "search_similar",
  "description": "Find records semantically similar using vector similarity search.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "description": { "type": "string" },
      "collection": { "type": "string" },
      "limit": { "type": "integer", "default": 10 },
      "threshold": { "type": "number", "default": 0.7 }
    },
    "required": ["description", "collection"]
  }
}
```

#### list_collections
List all available data collections (tables, API endpoints).
```json
{
  "name": "list_collections",
  "description": "List all available data collections that can be queried.",
  "inputSchema": { "type": "object", "properties": { "category": { "type": "string" } } }
}
```

#### describe_collection
Get detailed schema information for a specific collection.
```json
{
  "name": "describe_collection",
  "description": "Get detailed schema information for a specific collection.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "collection": { "type": "string" },
      "includeSamples": { "type": "boolean", "default": false }
    },
    "required": ["collection"]
  }
}
```

#### export_data
Export query results in specified format.
```json
{
  "name": "export_data",
  "description": "Export query results in specified format.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "format": { "type": "string", "enum": ["csv", "json", "xlsx"], "default": "csv" },
      "filename": { "type": "string" }
    },
    "required": ["query", "format"]
  }
}
```

### 3.3 Resource Definitions

```json
{ "uri": "schema://dataset/collections", "name": "Dataset Schema", "mimeType": "application/json" }
{ "uri": "schema://dataset/collections/{collection_name}", "name": "Collection Schema", "mimeType": "application/json" }
{ "uri": "catalog://metrics", "name": "Available Metrics", "mimeType": "application/json" }
{ "uri": "metadata://usage", "name": "Usage Statistics", "mimeType": "application/json" }
```

---

## 4. Data Model

### 4.1 Core Entities

```sql
-- Query history and audit log
CREATE TABLE query_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    question TEXT NOT NULL,
    intent VARCHAR(100),
    tools_used JSONB,
    result_summary TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector embeddings for RAG
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- API credentials (encrypted at rest)
CREATE TABLE api_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    auth_type VARCHAR(50),
    encrypted_headers JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collection/table registry
CREATE TABLE collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    schema_definition JSONB,
    category VARCHAR(100),
    is_vectorized BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.2 Indexes

```sql
CREATE INDEX idx_embeddings_collection ON embeddings(collection);
CREATE INDEX idx_embeddings_vector ON embeddings USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_query_logs_user ON query_logs(user_id);
CREATE INDEX idx_query_logs_created ON query_logs(created_at DESC);
```

---

## 5. API Design

### 5.1 MCP Protocol Endpoints (HTTP/SSE)

| Method | Path | Description |
|--------|------|-------------|
| POST | /mcp/v1/ | MCP JSON-RPC 2.0 message handler |
| GET | /mcp/v1/stream | SSE stream for server-push notifications |
| GET | /mcp/v1/capabilities | Server capability declaration |

### 5.2 Supplementary REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /api/v1/collections | List all collections |
| GET | /api/v1/collections/{name} | Describe a collection |
| GET | /api/v1/query-logs | Query audit log |
| POST | /api/v1/query-logs | Manually log a query |

### 5.3 Authentication

- MCP protocol: API key in `Authorization: Bearer <key>` header
- REST endpoints: API key authentication
- Internal API credentials stored encrypted in `api_credentials` table
- All requests logged to `query_logs` for audit

---

## 6. Agent Design

### 6.1 Query Understanding Agent

**Role:** Parse natural-language input into structured query plans.

**Prompt:**
```
You are a query understanding agent. Given a user's natural-language question
about their data, extract:
1. Intent: lookup | aggregation | comparison | summary | search_similar
2. Entities: table/collection names, field names, date ranges
3. Filters: any WHERE conditions expressed
4. Output format: concise | detailed | table | json

Respond with a valid JSON object matching the tool input schemas.
```

### 6.2 Data Retrieval Agent

**Role:** Execute the structured query against the internal API.

**Behavior:**
1. Look up collection schema from `collections` table
2. Build API request to internal endpoint
3. Execute with retry logic (3 attempts, exponential backoff)
4. Cache results in Redis with 5-minute TTL
5. Return raw results + metadata

### 6.3 Response Synthesis Agent

**Role:** Convert structured data results into natural-language answers.

**Prompt:**
```
You are a data analyst assistant. Given:
- User's original question
- Retrieved data results
- Source citations

Generate a clear, accurate response that:
1. Directly answers the question
2. Uses the data to support the answer
3. Cites sources using [n] notation
4. Indicates confidence when data is incomplete
5. Explains any caveats or limitations
```

---

## 7. Deployment

### 7.1 Docker Configuration

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "mcp.server"]
```

### 7.2 Docker Compose

```yaml
services:
  mcp-server:
    build: .
    ports: ["8000:8000"]
    environment:
      - INTERNAL_API_URL=${INTERNAL_API_URL}
      - INTERNAL_API_KEY=${INTERNAL_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - MCP_API_KEY=${MCP_API_KEY}
    depends_on:
      - postgres
      - redis

  postgres:
    image: pgvector/pgvector:pg15
    environment:
      - POSTGRES_DB=mcp_server
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### 7.3 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| INTERNAL_API_URL | Base URL of client's internal API | Yes |
| INTERNAL_API_KEY | API key for internal API | Yes |
| DATABASE_URL | PostgreSQL connection string | Yes |
| REDIS_URL | Redis connection string | Yes |
| ANTHROPIC_API_KEY | Anthropic API key for LLM calls | Yes |
| MCP_API_KEY | API key for MCP client authentication | Yes |
| LOG_LEVEL | Logging level (default: INFO) | No |

---

## 8. Acceptance Criteria

### 8.1 MCP Protocol Compliance

- [ ] Server responds to `initialize` with correct capabilities
- [ ] `tools/list` returns all 6 defined tools
- [ ] `tools/call` executes each tool and returns structured results
- [ ] `resources/list` returns all resource URIs
- [ ] Protocol handles invalid requests gracefully with error responses

### 8.2 Functional Requirements

- [ ] Natural-language queries return accurate data from internal API
- [ ] Aggregation queries (count, sum, avg) produce correct results
- [ ] Vector similarity search returns semantically relevant results
- [ ] Collection listing and description are accurate
- [ ] Data export produces valid CSV/JSON/XLSX files
- [ ] Query results are cached and returned within 100ms on cache hit

### 8.3 Non-Functional Requirements

- [ ] MCP endpoint responds within 5s for 95th percentile queries
- [ ] Server handles 100 concurrent MCP connections
- [ ] All queries are logged with user ID, timestamp, and result summary
- [ ] API credentials are never logged or exposed in responses
- [ ] Docker Compose stack starts successfully with `docker compose up`

### 8.4 Code Quality

- [ ] All Python modules pass `ruff` linting
- [ ] Type hints on all public function signatures
- [ ] Unit tests for tool handlers, agent prompts, and data models
- [ ] README with quickstart, architecture diagram, and API reference
