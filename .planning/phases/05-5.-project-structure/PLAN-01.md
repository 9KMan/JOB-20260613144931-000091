# Phase 05: 5. Project Structure

## Phase Goal
Implementation: code files, directory layout, tests

## Directory Structure
```
src/
  connector.ts     # OAuth + token management
  rest-client.ts   # REST API calls
  websocket.ts     # WebSocket with backoff
  types.ts         # TypeScript definitions
  risk/
    engine.ts      # Breach detection
  data/
    pipeline.ts    # Event processing
  observability/
    logger.ts      # Structured logging
    sentry.ts       # Sentry integration
    health.ts       # Health endpoints
tests/
  connector.test.ts
  risk.test.ts
```

## Key Implementation Details
- TypeScript strict (no `any`)
- Exponential backoff for reconnection
- Encrypted token storage
- Idempotent event processing
