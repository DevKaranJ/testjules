from typing import List
from ..strategies.base import Strategy

class BacktestEngine:
    """
    Engine for simulating strategies on historical data.
    """

    def __init__(self, strategies: List[Strategy]):
        self.strategies = strategies

    def run(self, start_time: str, end_time: str):
        """
        Run the backtest loop over the specified time range.
        """
        print(f"Running backtest from {start_time} to {end_time}")
        pass
