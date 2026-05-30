# Project Memory

**Core Identity:**
This is a full-stack, institutional-grade cryptocurrency futures trading platform designed for quantitative strategy research, backtesting, and live execution.

**Key Components:**
- Event-driven Python backend (FastAPI, asyncio, ccxt).
- Next.js / React frontend dashboard with Lightweight Charts.
- Textual CLI (TUI) for terminal-based power users.
- Database persistence via SQLAlchemy (SQLite locally, PostgreSQL in Docker).
- Dockerized architecture.

**The Strategy Engine:**
Supports a 3-Way switch (Single, All, Multiple) to run 8 mathematical quant models (e.g. Kalman Filter Pairs, VPIN Toxicity, PCA Neutral).

**Risk Management:**
Enforces 1% max risk per trade, halts on 3 consecutive losses, and triggers a global shutdown at 5% daily drawdown.

**Important Notice for Agents:**
*Always read this MEMORY.md first to understand the context of the project before making code changes.*

---

## Repository Stats

- **Total files**: 60 source files
- **Python**: 32 files / 1,107 lines
- **TypeScript/TSX**: 6 files / 197 lines
- **Markdown docs**: 5 files / 347 lines
- **Tests**: 5 files (pytest)
- **Strategies**: 8 concrete + 1 ABC

## Active Decisions

| ID | Decision | Status |
|----|----------|--------|
| D-001 | Event-driven architecture with typed dataclass events | Active |
| D-002 | Strategy ABC pattern for unified strategy interface | Active |
| D-003 | 3-way strategy mode switch (single/all/multiple) | Active |
| D-004 | SQLite for dev, PostgreSQL for prod via SQLAlchemy | Active |
| D-005 | Abstract execution layer (backtest vs live) | Active |
| D-006 | RiskManager as gate before PositionManager | Active |
| D-007 | Zustand for frontend state + WebSocket | Active |
| D-008 | lightweight-charts for charting | Active |
| D-009 | Tailwind CSS 4 for styling | Active |
| D-010 | Textual for terminal UI | Active |

## Known Issues

1. Backtest engine uses `generate_mock_data()` without real market data fallback
2. Live executor has API key hardcoded in `__init__` (needs .env)
3. No authentication on FastAPI endpoints
4. No rate limiting on WebSocket broadcasts
5. Tests have sys.path hacks instead of proper package installs
6. CCXTProFeed requires asyncio loop management in live engine
7. No graceful shutdown for WebSocket connections
8. Position table doesn't refresh automatically from WebSocket
9. StrategyControlPanel doesn't send config changes back to backend
10. No database migration system (SQLAlchemy create_all only)

## Recent Changes

- 2026-05-30: Initial project memory system created
- 2026-05-30: Graphify knowledge graph generated (369 nodes, 563 edges, 37 communities)
- 2026-05-30: Full repository scan completed (60 source files, ~1,877 LOC)
