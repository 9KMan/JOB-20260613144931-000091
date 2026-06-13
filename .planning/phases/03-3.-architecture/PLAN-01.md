# Phase 03: 3. Architecture

## Phase Goal
Component design, API surface, data flow, error handling

## Architecture Components
1. **Connector** — OAuth flow, token management, REST + WebSocket client
2. **RiskEngine** — breach detection, force-liquidation triggers
3. **DataPipeline** — event processing, database writes
4. **Observability** — structured logging, Sentry, health endpoints

## API Design
- REST endpoints: /api/{resource}/*
- WebSocket: real-time event stream
- Error handling: exponential backoff, idempotent processing

## Data Flow
Events → Connector → RiskEngine → DB write → Real-time push → UI
