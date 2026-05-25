from typing import List, Dict, Any
from ..strategies.base import Strategy
from .manager import StrategyManager
from ..execution.risk_manager import RiskManager
from ..execution.live_executor import LiveExecutor
from ..data.database import SessionLocal, initialize_database
from ..data.models import TradeLog

class LiveEngine:
    """
    Engine for running strategies on live market data (paper or real trading).
    """

    def __init__(self, available_strategies: Dict[str, Strategy], risk_config: Dict[str, Any] = None, executor: LiveExecutor = None):
        self.strategy_manager = StrategyManager(available_strategies)
        self.risk_manager = RiskManager(risk_config)
        self.executor = executor # Inject configured CCXT executor
        initialize_database()

    def start(self):
        """
        Start the live execution loop.
        """
        print("Starting live engine...")
        pass

    def process_signals(self):
        """
        Polls signals from the strategy manager and passes them through the risk manager.
        """
        signals = self.strategy_manager.poll_signals()

        for strategy_name, signal in signals.items():
            if isinstance(signal, str) and "NO TRADE" in signal:
                continue # Skip weak setups

            if isinstance(signal, dict):
                # Run through risk manager
                is_approved = self.risk_manager.evaluate_signal(signal)
                if is_approved:
                    # Calculate position size if entry and stop loss are provided
                    if "entry" in signal and "stop_loss" in signal:
                        qty = self.risk_manager.calculate_position_size(signal["entry"], signal["stop_loss"])
                        signal["quantity"] = qty

                    print(f"Executing Trade for {strategy_name}: {signal}")
                    if self.executor:
                        symbol = signal.get("pair", signal.get("symbol", "BTC/USDT"))
                        direction = signal.get("direction", "buy").lower()
                        self.executor.submit_order(symbol, direction, "market", signal.get("quantity", 0.01))
                        self._save_trade_to_db(strategy_name, symbol, direction, signal.get("entry", 0), signal.get("quantity", 0.01))
                else:
                    print(f"Trade rejected by Risk Manager for {strategy_name}")

    def _save_trade_to_db(self, strategy_name: str, symbol: str, direction: str, price: float, quantity: float):
        db = SessionLocal()
        try:
            log = TradeLog(
                strategy_name=strategy_name,
                symbol=symbol,
                direction=direction,
                entry_price=price,
                exit_price=0.0, # Not exited yet
                quantity=quantity,
                pnl=0.0,
                fee=0.0,
                slippage=0.0
            )
            db.add(log)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"DB Error: {e}")
        finally:
            db.close()
