from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    database: str


class StrategyStatus(BaseModel):
    name: str
    status: str = Field(..., pattern="^(running|stopped)$")


class StrategyListResponse(BaseModel):
    strategies: Dict[str, str]


class BacktestRunResponse(BaseModel):
    id: int
    run_date: datetime
    strategies: str
    start_equity: float
    end_equity: float
    total_trades: int
    win_rate: float
    max_drawdown: float
    parameters: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class TradeLogResponse(BaseModel):
    id: int
    strategy_name: str
    symbol: str
    direction: str
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    fee: float
    slippage: float
    timestamp: datetime

    model_config = {"from_attributes": True}


class PlatformStatus(BaseModel):
    strategies: Dict[str, str]
    active_connections: int


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class ActionResponse(BaseModel):
    status: str
    strategy: str



