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

---

## Session Protocol

### Start of session:
1. Read `MEMORY.md` - project context, active decisions, known issues
2. Read `TASKS.md` - current task queue
3. Read `DECISIONS.md` - architecture rationale
4. Read `REPO_MAP.md` - file locations and criticality
5. Read `ARCHITECTURE.md` - system structure

### End of session:
1. Update `MEMORY.md` with any new info
2. Update `TASKS.md` (mark completed, add new)
3. Update `DECISIONS.md` if new decisions made
4. Save session log to `logs/`

## Code Search Priority
1. Exact symbol lookup (grep for class/function name)
2. `API_MAP.md` / `REPO_GRAPH.md` for dependency info
3. `REPO_MAP.md` for file criticality
4. Full file read (last resort)

## Known Patterns

### Strategy Pattern
All strategies follow: `__init__` → `on_tick`/`on_orderbook` → `generate_signal`
New strategies need: inherit `Strategy`, implement 3 methods, add to `backend/strategies/`

### Event Pipeline
`MarketEvent` → `SignalEvent` → `OrderEvent` → `FillEvent` (all dataclasses)

### 3-Way Switch
`MODE_SINGLE=1`: one strategy by name
`MODE_ALL=2`: all strategies
`MODE_MULTIPLE=3`: named subset
