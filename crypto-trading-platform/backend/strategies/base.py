from abc import ABC, abstractmethod
from typing import Any, Dict


class Strategy(ABC):
    """
    Base Strategy Interface.
    All custom strategies should inherit from this class.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    @abstractmethod
    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        """
        Called when new tick data (trades) arrives.
        """
        pass

    @abstractmethod
    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        """
        Called when new orderbook snapshot/update arrives.
        """
        pass

    @abstractmethod
    def generate_signal(self) -> Any:
        """
        Evaluate current state and generate a trading signal if appropriate.
        """
        pass
