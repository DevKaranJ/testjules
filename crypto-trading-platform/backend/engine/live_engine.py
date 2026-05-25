from typing import List, Dict, Any
from ..strategies.base import Strategy
from .manager import StrategyManager
from ..execution.risk_manager import RiskManager

class LiveEngine:
    """
    Engine for running strategies on live market data (paper or real trading).
    """

    def __init__(self, available_strategies: Dict[str, Strategy], risk_config: Dict[str, Any] = None):
        self.strategy_manager = StrategyManager(available_strategies)
        self.risk_manager = RiskManager(risk_config)
        self.executor = None # To be injected later

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
                    # self.executor.submit_order(...)
                else:
                    print(f"Trade rejected by Risk Manager for {strategy_name}")
