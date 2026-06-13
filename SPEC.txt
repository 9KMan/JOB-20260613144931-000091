# Specification: Build an MCP Server on top of client's internal API plus a set of prompt-driven AI agents that answer natural-language questions against the connected dataset. Agents must search, retrieve, summarize,

## 1. Project Overview

**Project:** Build an MCP Server on top of client's internal API plus a set of prompt-driven AI agents that answer natural-language questions against the connected dataset. Agents must search, retrieve, summarize,
**GitHub:** https://github.com/9KMan/JOB-20260613144931-000091
**Lead:** https://www.upwork.com/jobs/~022065643599854241267
**Client:** Internal API Owner (Upwork, Featured Job)
**Tier:** LARGE
**Budget:** $25-150/hr hourly, contract-to-hire
**Rate:** $25/hr

## 2. Technical Stack

MCP · Python · Claude · API integration · RAG

## 3. Architecture

- AI/ML: Model integration (OpenAI API or similar)
- AI Pipeline: Data processing + inference + evaluation

### API Design
- RESTful endpoints with JSON request/response
- Authentication via JWT (HS256) or bcrypt
- Middleware for logging, error handling, CORS
- Versioned routes (/api/v1/...)

### Data Layer
- PostgreSQL as primary datastore
- Connection pooling via PGBouncer or similar
- Migration management via Alembic or raw SQL
- Indexes on foreign keys and high-cardinality columns

### Frontend (if applicable)
- Single-page application or server-rendered pages
- Responsive UI with modern CSS/JS framework
- State management for complex client-side logic

## 4. Data Model

### Core Entities
- Define entity schema based on job requirements
- Use UUIDs for primary keys (not auto-increment)
- Add created_at / updated_at timestamps to all tables
- Soft-delete pattern where appropriate

### Relationships
- Foreign key constraints with ON DELETE CASCADE
- Many-to-many via junction tables
- Eager loading for nested relationships in API

## 5. Project Structure

```
├── api/                  # FastAPI / Express routes + schemas
├── models/               # DB models / SQLAlchemy / Prisma
├── services/             # Business logic layer
├── workers/              # Background jobs (Celery, BullMQ, etc.)
├── migrations/           # DB migrations (Alembic / Flyway)
├── tests/                # Unit + integration tests
├── Dockerfile            # Production container
├── docker-compose.yml     # Local dev environment
└── README.md             # Setup instructions
```

## 6. Out of Scope

- Mobile apps (web only unless specified)
- Third-party integrations not mentioned in requirements
- Performance optimization at scale (1M+ users)
- White-label / multi-tenant unless explicitly required

## 7. Acceptance Criteria

- [ ] REST API with all planned endpoints implemented
- [ ] Frontend UI implemented and responsive
- [ ] AI/ML pipeline integrated and functional

**GitHub:** https://github.com/9KMan/JOB-20260613144931-000091
