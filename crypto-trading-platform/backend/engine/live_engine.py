from typing import List
from ..strategies.base import Strategy

class LiveEngine:
    """
    Engine for running strategies on live market data (paper or real trading).
    """

    def __init__(self, strategies: List[Strategy]):
        self.strategies = strategies

    def start(self):
        """
        Start the live execution loop.
        """
        print("Starting live engine...")
        pass
