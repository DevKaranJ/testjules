from typing import Dict, Any, List
from .models import FeeModel, SlippageModel

class Position:
    """
    Represents an open trading position.
    """
    def __init__(self, strategy_name: str, symbol: str, direction: str, entry_price: float, quantity: float, stop_loss: float, take_profit: float):
        self.strategy_name = strategy_name
        self.symbol = symbol
        self.direction = direction.upper() # 'LONG' or 'SHORT'
        self.entry_price = entry_price
        self.quantity = quantity
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        self.total_fees_paid = 0.0
        self.total_slippage = 0.0
        self.is_open = True

    def unrealized_pnl(self, current_price: float) -> float:
        if self.direction == 'LONG':
            return (current_price - self.entry_price) * self.quantity
        elif self.direction == 'SHORT':
            return (self.entry_price - current_price) * self.quantity
        return 0.0

class PositionManager:
    """
    Tracks and updates open positions based on incoming ticks.
    """
    def __init__(self, fee_model: FeeModel = None, slippage_model: SlippageModel = None):
        self.positions: List[Position] = []
        self.closed_trades: List[Dict[str, Any]] = []
        self.fee_model = fee_model or FeeModel()
        self.slippage_model = slippage_model or SlippageModel()

    def open_position(self, strategy_name: str, symbol: str, direction: str, price: float, quantity: float, stop_loss: float, take_profit: float):
        """
        Simulates entering a position, applying slippage and fees.
        """
        slippage = self.slippage_model.calculate_slippage(price, quantity, "market")

        # Adjust entry price based on slippage
        actual_entry = price + slippage if direction.upper() == 'LONG' else price - slippage
        fee = self.fee_model.calculate_fee(actual_entry, quantity, is_maker=False)

        pos = Position(strategy_name, symbol, direction, actual_entry, quantity, stop_loss, take_profit)
        pos.total_fees_paid += fee
        pos.total_slippage += slippage * quantity

        self.positions.append(pos)
        return fee, slippage

    def update(self, tick: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Updates all open positions with the current price.
        Closes positions if TP or SL is hit.
        Returns a list of newly closed trade logs.
        """
        current_price = tick["price"]
        symbol = tick.get("symbol", "BTC/USDT") # Default for simulation

        newly_closed = []

        for pos in self.positions[:]:
            if not pos.is_open or pos.symbol != symbol:
                continue

            close_reason = None

            if pos.direction == 'LONG':
                if current_price <= pos.stop_loss:
                    close_reason = "STOP_LOSS"
                elif current_price >= pos.take_profit:
                    close_reason = "TAKE_PROFIT"
            elif pos.direction == 'SHORT':
                if current_price >= pos.stop_loss:
                    close_reason = "STOP_LOSS"
                elif current_price <= pos.take_profit:
                    close_reason = "TAKE_PROFIT"

            if close_reason:
                trade_log = self._close_position(pos, current_price, close_reason)
                newly_closed.append(trade_log)

        return newly_closed

    def _close_position(self, pos: Position, current_price: float, reason: str) -> Dict[str, Any]:
        """
        Closes a position, applies exit fees/slippage, and calculates final PnL.
        """
        slippage = self.slippage_model.calculate_slippage(current_price, pos.quantity, "market")
        actual_exit = current_price - slippage if pos.direction == 'LONG' else current_price + slippage

        fee = self.fee_model.calculate_fee(actual_exit, pos.quantity, is_maker=False)

        pos.total_fees_paid += fee
        pos.total_slippage += slippage * pos.quantity

        # Calculate gross PnL
        if pos.direction == 'LONG':
            gross_pnl = (actual_exit - pos.entry_price) * pos.quantity
        else:
            gross_pnl = (pos.entry_price - actual_exit) * pos.quantity

        net_pnl = gross_pnl - pos.total_fees_paid

        pos.is_open = False
        self.positions.remove(pos)

        trade_log = {
            "strategy": pos.strategy_name,
            "symbol": pos.symbol,
            "direction": pos.direction,
            "entry_price": pos.entry_price,
            "exit_price": actual_exit,
            "quantity": pos.quantity,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "fees": pos.total_fees_paid,
            "slippage": pos.total_slippage,
            "reason": reason
        }
        self.closed_trades.append(trade_log)
        return trade_log
