from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DataTable, Log
from textual.containers import Grid
import sys
import os

# Ensure backend imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.data.database import SessionLocal
from backend.data.models import TradeLog

class DashboardApp(App):
    """A Textual Dashboard for the Crypto Trading Platform."""

    CSS = """
    Grid {
        grid-size: 2;
        grid-columns: 1fr 2fr;
    }

    #strategies-panel {
        height: 100%;
        border: solid green;
    }

    #logs-panel {
        height: 100%;
        border: solid blue;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Grid():
            # Left Panel: Strategies
            table = DataTable(id="strategies-panel")
            table.add_columns("Strategy", "Symbol", "Entry", "PnL")
            yield table

            # Right Panel: Logs
            log = Log(id="logs-panel")
            log.write_line("System initialized.")
            log.write_line("Connected to database.")
            yield log

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        db = SessionLocal()
        try:
            trades = db.query(TradeLog).order_by(TradeLog.id.desc()).limit(20).all()
            for t in trades:
                table.add_row(t.strategy_name, t.symbol, str(t.entry_price), f"${t.pnl:.2f}")
            log.write_line(f"Loaded {len(trades)} recent trades from Database.")
        except Exception as e:
            log.write_line(f"DB Error: {e}")
        finally:
            db.close()

        yield Footer()

def run_app():
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    run_app()
