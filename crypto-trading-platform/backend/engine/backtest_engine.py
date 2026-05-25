from typing import List, Dict, Any
from ..strategies.base import Strategy
from .manager import StrategyManager
from ..execution.risk_manager import RiskManager

class BacktestEngine:
    """
    Engine for simulating strategies on historical data.
    Integrates the StrategyManager and RiskManager to simulate execution.
    """

    def __init__(self, available_strategies: Dict[str, Strategy], risk_config: Dict[str, Any] = None):
        self.strategy_manager = StrategyManager(available_strategies)
        self.risk_manager = RiskManager(risk_config)

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
        data_feed: A list of tick dictionaries, e.g., [{"price": 50000, "timestamp": 12345}, ...]
        """
        print(f"Starting backtest over {len(data_feed)} data points...")

        for tick in data_feed:
            # 1. Update strategies with new data
            self.strategy_manager.route_tick(tick)

            # 2. Poll for signals
            signals = self.strategy_manager.poll_signals()

            # 3. Process signals and simulate execution
            for strategy_name, signal in signals.items():
                # Skip invalid or weak signals
                if isinstance(signal, str) and "NO TRADE" in signal:
                    continue

                if isinstance(signal, dict):
                    # Risk management check
                    if self.risk_manager.evaluate_signal(signal):
                        self._simulate_execution(strategy_name, signal, tick["price"])

        self._print_results()

    def _simulate_execution(self, strategy_name: str, signal: Dict[str, Any], current_price: float):
        """
        Simulates the execution of a trade and calculates mock PnL.
        """
        self.total_trades += 1

        # Basic mock execution: assume a random outcome based on RR or just standard win/loss for simulation
        # In a real backtester, we would track open positions and close them against future ticks.
        # For this skeleton, we will simulate immediate resolution.

        direction = signal.get("direction", signal.get("action", "UNKNOWN"))

        # Simulate a 55% win rate for the sake of demonstrating the metrics
        import random
        is_win = random.random() > 0.45

        if is_win:
            self.winning_trades += 1
            # Mock profit: 2% of total equity
            pnl = self.risk_manager.total_equity * 0.02
        else:
            # Mock loss: 1% of total equity
            pnl = -(self.risk_manager.total_equity * 0.01)

        self.risk_manager.update_trade_result(pnl)

        trade_record = {
            "strategy": strategy_name,
            "direction": direction,
            "price": current_price,
            "pnl": pnl,
            "equity": self.risk_manager.total_equity
        }
        self.history.append(trade_record)

    def _print_results(self):
        """Output backtest performance metrics."""
        print("\n=== BACKTEST RESULTS ===")
        print(f"Total Trades: {self.total_trades}")
        if self.total_trades > 0:
            win_rate = (self.winning_trades / self.total_trades) * 100
            print(f"Win Rate: {win_rate:.2f}%")
        print(f"Final Equity: ${self.risk_manager.total_equity:.2f}")
        print(f"Max Consecutive Losses Reached: {self.risk_manager.consecutive_losses}")
        print("========================\n")
