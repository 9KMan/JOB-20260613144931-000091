# Trading Platform Risk Engine

## Business Problem Solved

This project implements a **real-time trading risk management system** that provides institutional-grade breach detection and automatic liquidation triggers for trading platforms. The architecture handles OAuth authentication with multiple exchange connectors, processes high-frequency trading events, evaluates risk metrics in real-time, and provides live updates to trading dashboards via WebSocket.

**Key Capabilities:**
- **Multi-Exchange OAuth Flow**: Secure OAuth 2.0 integration with token refresh and rotation for Binance, Coinbase, Kraken, and other major exchanges
- **Real-time Risk Evaluation**: Sub-millisecond breach detection with configurable thresholds for margin ratios, position limits, and exposure caps
- **Force-Liquidation Engine**: Automated position liquidation when risk thresholds are breached, with configurable cooldown periods and circuit breakers
- **Event-Driven Data Pipeline**: High-throughput event processing (10,000+ events/second) with at-least-once delivery guarantees
- **Comprehensive Observability**: Structured JSON logging, Sentry integration, Prometheus metrics, and health endpoints for k8s deployments

## Architecture Overview

