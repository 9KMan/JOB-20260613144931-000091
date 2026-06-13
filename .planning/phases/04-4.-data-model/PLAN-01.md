# Phase 04: Data Model

## Phase Goal
Create the PostgreSQL schema (SQLite-compatible for PoC) for collections, embeddings, credentials, and query logs.

## Preconditions
- Phase 2 complete (database session ready)

## Tasks
- [ ] Create `alembic/versions/001_initial_schema.py` — collections, query_logs, embeddings, api_credentials tables
- [ ] Add UUID primary keys and created_at timestamps to all tables
- [ ] Create GIN indexes on text columns (query_logs.question, embeddings.content)
- [ ] Seed `scripts/seed_collections.py` — populate collections table with placeholder entries
- [ ] Create `src/mcp_server/models.py` — SQLAlchemy ORM models matching schema

## Deliverables
- `alembic/versions/001_initial_schema.py`
- `scripts/seed_collections.py`
- `src/mcp_server/models.py`

## Verification
- [ ] `alembic upgrade head` creates all tables without errors
- [ ] ORM models import without errors
- [ ] Seed script populates at least 2 collections
