# Agent Notes (For OpenCode and Future AI Assistants)

## Directives
- **Always read `MEMORY.md` first** before making any code changes.
- **Always update `TASKS.md`** after implementing new features or fixing bugs.
- **Store architecture decisions in `DECISIONS.md`.**

## Common Commands
- **Run Backend Tests**: `python -m pytest backend/tests/ tui/`
- **Run Backtester**: `python run_backtest.py`
- **Start API Server**: `uvicorn backend.api.main:app --host 0.0.0.0 --port 8000`
- **Start React Frontend**: `cd frontend && npm run dev`
- **Start Terminal UI**: `python tui/app.py`
- **Run Docker Stack**: `docker-compose up --build`

## Context Reminders
- The codebase uses `ccxt` for fetching real historical data and `ccxtpro` for live WebSockets.
- The React frontend strictly uses Next.js 14 and React 18 to avoid dependency conflicts.
- Do not commit `.db` files or `__pycache__` to the repository.