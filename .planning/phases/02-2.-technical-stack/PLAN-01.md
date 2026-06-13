# Phase 02: 2. Technical Stack

## Phase Goal
Dependencies, architecture, integration points

## Technical Architecture
- REST + WebSocket dual protocol
- OAuth 2.0 with encrypted token storage
- Exponential backoff reconnection
- Rate limit handling (429 + penalty ticket)

## Dependencies
```json
{
  "dependencies": {
    "ws": "^8.16.0",
    "axios": "^1.6.0",
    "pg": "^8.11.0",
    "dotenv": "^16.4.0"
}}

## Infrastructure
- Docker Compose with health checks
- Traefik SSL termination
- GitHub Actions CI/CD
- Sentry error tracking
