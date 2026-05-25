from typing import List, Dict, Any
from ..strategies.base import Strategy
from .manager import StrategyManager
from ..execution.risk_manager import RiskManager
from ..execution.position_manager import PositionManager
from ..execution.models import FeeModel, SlippageModel

class BacktestEngine:
    """
    Engine for simulating strategies on historical data.
    Integrates StrategyManager, RiskManager, and PositionManager for realistic execution.
    """

    def __init__(self, available_strategies: Dict[str, Strategy], risk_config: Dict[str, Any] = None):
        self.strategy_manager = StrategyManager(available_strategies)
        self.risk_manager = RiskManager(risk_config)
        self.position_manager = PositionManager(FeeModel(), SlippageModel())

        # State tracking for backtest
        self.history = []
        self.total_trades = 0
        self.winning_trades = 0

    def set_mode(self, mode: int, selected_strategy_names: List[str] = None):
        """Configure which strategies to run during the backtest."""
        self.strategy_manager.set_mode(mode, selected_strategy_names)

    def run(self, data_feed: List[Dict[str, Any]]):
        """
        Run the backtest loop over the provided historical data stream.
        """
        print(f"Starting backtest over {len(data_feed)} data points...")

        for tick in data_feed:
            # 1. Update open positions and check for SL/TP hits
            closed_trades = self.position_manager.update(tick)
            for trade in closed_trades:
                self._record_closed_trade(trade)

            # 2. Update strategies with new data
            self.strategy_manager.route_tick(tick)

            # 3. Poll for signals
            signals = self.strategy_manager.poll_signals()

            # 4. Process signals and simulate entering execution
            for strategy_name, signal in signals.items():
                if isinstance(signal, str) and "NO TRADE" in signal:
                    continue

                if isinstance(signal, dict):
                    if self.risk_manager.evaluate_signal(signal):
                        self._execute_entry(strategy_name, signal, tick["price"])

        # Force close any remaining open positions at the end of the data feed
        if len(data_feed) > 0:
            final_tick = data_feed[-1]
            for pos in list(self.position_manager.positions):
                trade_log = self.position_manager._close_position(pos, final_tick["price"], "END_OF_BACKTEST")
                self._record_closed_trade(trade_log)

        self._print_results()

    def _execute_entry(self, strategy_name: str, signal: Dict[str, Any], current_price: float):
        """
        Processes an approved signal and opens a position via the PositionManager.
        """
        direction = signal.get("direction", signal.get("action", "UNKNOWN")).upper()
        if direction not in ["LONG", "SHORT"]:
            # Fallback for strategies that don't output explicit long/short
            direction = "LONG" if "LONG" in direction else "SHORT"

        entry_price = signal.get("entry", current_price)
        stop_loss = signal.get("stop_loss", current_price * 0.95 if direction == 'LONG' else current_price * 1.05)
        take_profit = signal.get("take_profit", current_price * 1.10 if direction == 'LONG' else current_price * 0.90)

        # Calculate size based on risk manager
        quantity = self.risk_manager.calculate_position_size(entry_price, stop_loss)
        if quantity <= 0:
            return

        # Deduct initial fees from equity
        entry_fee, slippage = self.position_manager.open_position(
            strategy_name, "BTCUSDT", direction, entry_price, quantity, stop_loss, take_profit
        )
        self.risk_manager.total_equity -= entry_fee

    def _record_closed_trade(self, trade: Dict[str, Any]):
        """
        Processes a trade completed by the PositionManager.
        """
        self.total_trades += 1
        net_pnl = trade["net_pnl"]

        if net_pnl > 0:
            self.winning_trades += 1

        self.risk_manager.update_trade_result(net_pnl)

        trade["equity"] = self.risk_manager.total_equity
        self.history.append(trade)

    def _print_results(self):
        """Output backtest performance metrics."""
        print("\n=== BACKTEST RESULTS ===")
        print(f"Total Trades Executed: {self.total_trades}")
        if self.total_trades > 0:
            win_rate = (self.winning_trades / self.total_trades) * 100
            print(f"Win Rate: {win_rate:.2f}%")
        print(f"Final Equity: ${self.risk_manager.total_equity:.2f}")
        print(f"Max Consecutive Losses Reached: {self.risk_manager.consecutive_losses}")
        print("========================\n")
