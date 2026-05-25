from ..core.events import OrderEvent

class Executor:
    """
    Base Executor class for handling order placement.
    """

    def submit_order(self, order: OrderEvent):
        """
        Submit an order to the exchange (or paper trading simulator).
        """
        pass

    def cancel_order(self, order_id: str):
        pass
