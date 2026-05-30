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