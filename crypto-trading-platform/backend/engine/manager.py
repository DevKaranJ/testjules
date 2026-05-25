from typing import Dict, List, Any
from ..strategies.base import Strategy

class StrategyManager:
    """
    Manages the initialization and routing of data to strategies.
    Supports a 3-way switch mechanism for operating modes.
    """

    MODE_SINGLE = 1
    MODE_ALL = 2
    MODE_MULTIPLE = 3

    def __init__(self, available_strategies: Dict[str, Strategy]):
        """
        available_strategies: A dictionary mapping strategy names to Strategy instances.
        """
        self.available_strategies = available_strategies
        self.active_strategies: Dict[str, Strategy] = {}
        self.mode = None

    def set_mode(self, mode: int, selected_strategy_names: List[str] = None):
        """
        Configures the manager based on the 3-way switch.

        Option 1 (MODE_SINGLE): Switch on only 1 strategy.
        Option 2 (MODE_ALL): Switch on all strategies.
        Option 3 (MODE_MULTIPLE): Switch on multiple specific strategies.
        """
        self.active_strategies.clear()
        self.mode = mode

        if mode == self.MODE_SINGLE:
            if not selected_strategy_names or len(selected_strategy_names) != 1:
                raise ValueError("MODE_SINGLE requires exactly one strategy name.")
            name = selected_strategy_names[0]
            if name in self.available_strategies:
                self.active_strategies[name] = self.available_strategies[name]
            else:
                raise ValueError(f"Strategy {name} not found.")

        elif mode == self.MODE_ALL:
            self.active_strategies = dict(self.available_strategies)

        elif mode == self.MODE_MULTIPLE:
            if not selected_strategy_names or len(selected_strategy_names) < 1:
                raise ValueError("MODE_MULTIPLE requires at least one strategy name.")
            for name in selected_strategy_names:
                if name in self.available_strategies:
                    self.active_strategies[name] = self.available_strategies[name]
                else:
                    raise ValueError(f"Strategy {name} not found.")
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def route_tick(self, tick_data: Dict[str, Any]):
        """
        Routes tick data to all active strategies.
        """
        for name, strategy in self.active_strategies.items():
            strategy.on_tick(tick_data)

    def route_orderbook(self, orderbook_data: Dict[str, Any]):
        """
        Routes orderbook data to all active strategies.
        """
        for name, strategy in self.active_strategies.items():
            strategy.on_orderbook(orderbook_data)

    def poll_signals(self) -> Dict[str, Any]:
        """
        Polls all active strategies for signals.
        """
        signals = {}
        for name, strategy in self.active_strategies.items():
            signal = strategy.generate_signal()
            if signal:
                signals[name] = signal
        return signals
