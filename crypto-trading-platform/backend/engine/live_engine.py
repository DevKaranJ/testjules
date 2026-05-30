import asyncio
import time
from typing import List, Dict, Any, Optional, Callable
from structlog import get_logger

from ..strategies.base import Strategy
from .manager import StrategyManager
from ..execution.risk_manager import RiskManager
from ..execution.live_executor import LiveExecutor
from ..execution.models import FeeModel, SlippageModel
from ..execution.position_manager import PositionManager
from ..data.database import SessionLocal, initialize_database
from ..data.models import TradeLog

logger = get_logger()


class LiveEngine:
    """
    Engine for running strategies on live market data with order confirmation and position sync.
    """

    def __init__(
        self,
        available_strategies: Dict[str, Strategy],
        risk_config: Optional[Dict[str, Any]] = None,
        executor: Optional[LiveExecutor] = None,
        on_trade: Optional[Callable] = None,
    ):
        self.strategy_manager = StrategyManager(available_strategies)
        self.risk_manager = RiskManager(risk_config)
        self.executor = executor
        self.position_manager = PositionManager(FeeModel(), SlippageModel())
        self.on_trade = on_trade or (lambda t: None)
        self._running = False
        initialize_database()

    async def start(self, market_data_queue: asyncio.Queue):
        """Start the live execution loop reading from a market data queue."""
        logger.info("live_engine_starting")
        self._running = True
        while self._running:
            try:
                tick = await asyncio.wait_for(market_data_queue.get(), timeout=1.0)
                await self._process_tick(tick)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error("live_engine_error", error=str(e))

    def stop(self):
        logger.info("live_engine_stopping")
        self._running = False

    async def _process_tick(self, tick: Dict[str, Any]):
        """Process a single market data tick through the entire pipeline."""
        # 1. Update open positions via PositionManager
        self.position_manager.update(tick)

        # 2. Route tick to strategies
        self.strategy_manager.route_tick(tick)

        # 3. Poll signals
        signals = self.strategy_manager.poll_signals()

        # 4. Process each signal
        for strategy_name, signal in signals.items():
            if isinstance(signal, str) and "NO TRADE" in signal:
                continue

            if not isinstance(signal, dict):
                continue

            if not self.risk_manager.evaluate_signal(signal):
                continue

            await self._execute_signal(strategy_name, signal, tick.get("price", 0))

    async def _execute_signal(self, strategy_name: str, signal: Dict[str, Any], current_price: float):
        """Execute a trading signal: validate, size, submit order, confirm, log."""
        direction = signal.get("direction", "").upper()
        if direction not in ("LONG", "SHORT"):
            return

        entry = signal.get("entry", current_price)
        stop_loss = signal.get("stop_loss", entry * 0.95 if direction == "LONG" else entry * 1.05)
        take_profit = signal.get("take_profit", entry * 1.10 if direction == "LONG" else entry * 0.90)
        symbol = signal.get("symbol", signal.get("pair", "BTC/USDT"))
        quantity = self.risk_manager.calculate_position_size(entry, stop_loss)

        if quantity <= 0:
            return

        logger.info("executing_signal", strategy=strategy_name, symbol=symbol, direction=direction, qty=quantity)

        # If we have a live executor, submit the order and confirm
        if self.executor:
            result = self.executor.submit_order(symbol, direction.lower(), "market", quantity)
            order_id = result.get("id")
            if order_id:
                confirmed = self.executor.confirm_order(order_id, timeout=10.0)
                if confirmed:
                    fill_price = confirmed.get("price", entry)
                    filled_qty = confirmed.get("filled", quantity)
                else:
                    logger.warning("order_not_confirmed", order_id=order_id)
                    return
            else:
                return
        else:
            fill_price = entry
            filled_qty = quantity

        # Open position in PositionManager (for stop/take-profit tracking)
        fee, slippage = self.position_manager.open_position(
            strategy_name, symbol, direction, fill_price, filled_qty, stop_loss, take_profit
        )
        self.risk_manager.total_equity -= fee

        # Save to DB
        self._save_trade_to_db(strategy_name, symbol, direction, fill_price, filled_qty, fee)

        # Notify callback (e.g., WebSocket broadcast)
        self.on_trade({
            "type": "trade_executed",
            "strategy": strategy_name,
            "symbol": symbol,
            "direction": direction,
            "entry_price": fill_price,
            "quantity": filled_qty,
            "pnl": 0.0,
            "fee": fee,
            "timestamp": time.time(),
        })

    def _save_trade_to_db(self, strategy_name: str, symbol: str, direction: str,
                          price: float, quantity: float, fee: float):
        db = SessionLocal()
        try:
            log = TradeLog(
                strategy_name=strategy_name,
                symbol=symbol,
                direction=direction,
                entry_price=price,
                exit_price=0.0,
                quantity=quantity,
                pnl=0.0,
                fee=fee,
                slippage=0.0,
            )
            db.add(log)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error("trade_save_failed", error=str(e))
        finally:
            db.close()
