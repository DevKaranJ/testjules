# Repository Map

## File Index

### Root
| File | Purpose | Criticality |
|------|---------|-------------|
| `run_backtest.py` | CLI entry point for backtesting | High |
| `DESIGN.md` | Full architecture document | Medium |
| `FRONTEND_DESIGN.md` | UI/UX design document | Medium |
| `README.md` | Project overview | Low |
| `requirements.txt` | Python dependencies | High |
| `docker-compose.yml` | Container orchestration | Medium |

### Backend (`backend/`)

| File | Purpose | Criticality |
|------|---------|-------------|
| `api/main.py` | FastAPI server, WebSocket, REST endpoints | High |
| `core/events.py` | Event dataclasses (Market, Signal, Order, Fill) | High |
| `data/feed.py` | Abstract DataFeed base class | High |
| `data/ccxt_feed.py` | CCXT sync REST feed | High |
| `data/ccxt_pro_feed.py` | CCXT Pro async WebSocket feed | High |
| `data/models.py` | SQLAlchemy ORM models (TradeLog, BacktestRun) | High |
| `data/database.py` | SQLAlchemy engine + session factory | High |
| `engine/manager.py` | StrategyManager (3-way mode switch) | High |
| `engine/backtest_engine.py` | Historical backtesting simulation | High |
| `engine/live_engine.py` | Live/paper trading engine | High |
| `execution/executor.py` | Abstract Executor base | High |
| `execution/live_executor.py` | CCXT live order execution | High |
| `execution/models.py` | FeeModel, SlippageModel | High |
| `execution/position_manager.py` | Position tracking, SL/TP | High |
| `execution/risk_manager.py` | Risk controls | High |
| `strategies/base.py` | Strategy ABC | High |
| `strategies/kalman_pairs.py` | Kalman Filter pairs trading | Medium |
| `strategies/vpin_toxicity.py` | VPIN toxicity model | Medium |
| `strategies/pca_neutral.py` | PCA factor neutral | Medium |
| `strategies/mean_reversion.py` | Cross-sectional mean reversion | Medium |
| `strategies/hmm_regime.py` | HMM regime detection | Medium |
| `strategies/iv_crush.py` | Implied volatility crush | Medium |
| `strategies/dispersion_arb.py` | Dispersion vol arbitrage | Medium |
| `strategies/orderflow_scalping.py` | Order flow scalping | Medium |
| `tests/test_events.py` | Event dataclass tests | Medium |
| `tests/test_execution.py` | FeeModel + PositionManager tests | Medium |
| `tests/test_manager.py` | StrategyManager switch tests | Medium |
| `tests/test_risk_manager.py` | RiskManager tests | Medium |
| `tests/test_strategies.py` | Strategy instantiation tests | Medium |

### Frontend (`frontend/`)
| File | Purpose | Criticality |
|------|---------|-------------|
| `src/app/layout.tsx` | Root layout with Inter font | High |
| `src/app/page.tsx` | Dashboard page (composes all widgets) | High |
| `src/components/ChartWidget.tsx` | Candlestick chart (lightweight-charts) | High |
| `src/components/PositionTable.tsx` | Trade/position table | High |
| `src/components/StrategyControlPanel.tsx` | Strategy selector UI | High |
| `src/store/useStore.ts` | Zustand store + WebSocket client | High |
| `package.json` | Dependencies + scripts | High |
| `tsconfig.json` | TypeScript config | High |

### TUI (`tui/`)
| File | Purpose | Criticality |
|------|---------|-------------|
| `app.py` | Textual DashboardApp (DataTable + Log) | Medium |

### Infrastructure
| File | Purpose | Criticality |
|------|---------|-------------|
| `docker/backend.Dockerfile` | Python 3.12 backend container | Medium |
| `docker/frontend.Dockerfile` | Node 18 frontend container | Medium |
| `docker-compose.yml` | 3-service orchestration | Medium |

## Build & Run Commands

```bash
# Backend (dev)
pip install -r requirements.txt
uvicorn backend.api.main:app --reload

# Frontend (dev)
cd frontend && npm install && npm run dev

# Full stack (Docker)
docker compose up

# Run tests
python -m pytest backend/tests/ tui/

# Run backtest
python run_backtest.py

# Run TUI
python -m tui.app
```
