# Task Tracker

## Legend
- `[ ]` Pending
- `[/]` In Progress
- `[x]` Completed
- `[!]` Blocked

## Completed Tasks
- [x] Initial Repository Scaffolding
- [x] Core Event Engine and Interfaces
- [x] 8 Quant Strategies (Base Implementations)
- [x] 3-Way Strategy Switch
- [x] Global Risk Manager (Tilt protection, sizing)
- [x] Backtesting Simulator with Position Tracking, Slippage, and Fees
- [x] CCXT Integration (REST & Pro/WebSockets)
- [x] SQLAlchemy Database Models (SQLite/PostgreSQL)
- [x] FastAPI Server & WebSockets
- [x] Next.js Dashboard (React, Tailwind, Zustand, Lightweight Charts)
- [x] Python Textual TUI
- [x] Dockerization (docker-compose, backend.Dockerfile, frontend.Dockerfile)

## Pending Tasks

### Phase 1: Operational Polish
- [ ] Connect Next.js Dashboard buttons to API REST endpoints (Start/Stop strategies).
- [ ] Implement full deep-math parsing for all 8 strategies (e.g. strict footprint parsing for Scalping).
- [ ] Migrate SQLite development database to production PostgreSQL container permanently.
- [ ] Add advanced execution (Iceberg, VWAP) to LiveExecutor.
- [ ] Implement Authentication for FastAPI/Next.js to secure the dashboard.

### Phase 2: Code Quality & Fixes
- [ ] Move API keys/credentials to .env
- [ ] Remove sys.path hacks in tests (use pip install -e .)
- [ ] Add database migration system (Alembic)
- [ ] Add WebSocket rate limiting
- [ ] Add graceful shutdown for WebSocket connections
- [ ] Add auto-refresh to PositionTable from WebSocket
- [ ] Add real market data fallback when CCXT fails

### Phase 3: Testing
- [ ] Increase test coverage (currently ~5 files)
- [ ] Add integration tests for backtest engine
- [ ] Add integration tests for live engine
- [ ] Add WebSocket tests
- [ ] Add frontend component tests

### Phase 4: Documentation
- [ ] Add API docstrings to all endpoints
- [ ] Add strategy documentation
- [ ] Add deployment guide
- [ ] Add contribution guidelines

### Phase 5: Monitoring & Observability
- [ ] Add structured logging
- [ ] Add performance metrics
- [ ] Add error tracking
- [ ] Add health check endpoints

### Phase 6: CI/CD
- [ ] Add GitHub Actions workflow
- [ ] Add pre-commit hooks
- [ ] Add linting configuration
- [ ] Add type checking to CI

### Backlog
- [ ] Add ML-based signal generation
- [ ] Add portfolio-level risk management
- [ ] Add multi-exchange support
- [ ] Add real-time P&L tracking
- [ ] Add order book visualization
- [ ] Add strategy performance analytics
- [ ] Add backtest comparison tool
- [ ] Add Telegram/Discord notifications

*Always update TASKS.md after changes.*
