# Repository Graph

## Import Graph

```
run_backtest.py
  ├── BacktestEngine (engine/)
  │     ├── Strategy (strategies/)
  │     ├── StrategyManager (engine/)
  │     ├── RiskManager (execution/)
  │     ├── PositionManager (execution/)
  │     │     ├── FeeModel (execution/)
  │     │     └── SlippageModel (execution/)
  │     ├── database (data/)
  │     └── models (data/)
  ├── StrategyManager (engine/)
  └── CCXTFeed (data/)

backend/api/main.py
  ├── database.get_db (data/)
  └── models (data/)

tui/app.py
  ├── database.SessionLocal (data/)
  └── models.TradeLog (data/)
```

### Shared Module Dependencies

| Module | Imported By |
|--------|-------------|
| `strategies.base.Strategy` | manager, backtest_engine, live_engine, all 8 strategies, tests |
| `core.events.*` | ccxt_feed, ccxt_pro_feed, executor |
| `data.models.*` | backtest_engine, live_engine, api/main, tui/app |
| `data.database.*` | backtest_engine, live_engine, api/main, tui/app |
| `execution.risk_manager` | backtest_engine, live_engine |
| `execution.position_manager` | backtest_engine, live_engine |
| `engine.manager.StrategyManager` | backtest_engine, live_engine |

## Function Call Graph

### Backtest Flow
```
main() [run_backtest.py]
  ├── generate_mock_data()
  ├── StrategyManager.__init__() + set_mode()
  ├── BacktestEngine.__init__() + set_mode()
  └── BacktestEngine.run()
        ├── CCXTFeed.fetch_ohlcv()
        └── loop (per tick):
              ├── StrategyManager.route_tick()
              │     └── Strategy.on_tick()
              ├── StrategyManager.poll_signals()
              │     └── Strategy.generate_signal()
              ├── RiskManager.evaluate_signal()
              ├── PositionManager.open_position()
              ├── PositionManager.update()
              └── PositionManager._close_position()
        ├── _save_results_to_db()
        └── _print_results()
```

### Live Trading Flow
```
LiveEngine.start()
  └── loop:
        ├── StrategyManager.poll_signals()
        ├── RiskManager.evaluate_signal()
        ├── PositionManager.open_position()
        ├── LiveExecutor.submit_order()
        └── _save_trade_to_db()
```

### API Flow
```
FastAPI startup → startup_event() → asyncio.create_task(broadcast_market_state())
WebSocket connect → ConnectionManager.connect() → loop: receive → broadcast
REST: get_backtest_runs() / get_backtest_trades() → SQLAlchemy query
```

## Database Schema

```sql
CREATE TABLE trade_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_name VARCHAR NOT NULL,
    symbol VARCHAR NOT NULL,
    action VARCHAR NOT NULL,
    entry_price FLOAT NOT NULL,
    exit_price FLOAT,
    quantity FLOAT NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME,
    pnl FLOAT,
    pnl_pct FLOAT,
    status VARCHAR DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE backtest_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode INTEGER NOT NULL,
    strategies VARCHAR NOT NULL,
    symbol VARCHAR NOT NULL,
    total_trades INTEGER DEFAULT 0,
    total_pnl FLOAT DEFAULT 0,
    total_pnl_pct FLOAT DEFAULT 0,
    sharpe_ratio FLOAT,
    max_drawdown FLOAT,
    win_rate FLOAT,
    start_time DATETIME,
    end_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Component-Strategy Matrix

| Strategy | Type | Data Source |
|----------|------|-------------|
| KalmanPairsStrategy | Statistical arbitrage | Price ticks |
| VPINToxicityStrategy | Volume analysis | Order book |
| PCANeutralStrategy | Factor model | Price ticks |
| MeanReversionStrategy | Statistical | Price ticks |
| HMMRegimeStrategy | ML regime detection | Price ticks |
| IVCrushStrategy | Options theory | Price ticks |
| DispersionArbitrageStrategy | Vol arbitrage | Price ticks |
| OrderFlowScalpingStrategy | Order flow | Order book |
