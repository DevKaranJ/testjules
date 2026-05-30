from backend.strategies.base import Strategy

class DummyStrategy(Strategy):
    def on_tick(self, tick_data):
        pass
    def on_orderbook(self, orderbook_data):
        pass
    def generate_signal(self):
        return True

def test_strategy_instantiation():
    strategy = DummyStrategy(config={"threshold": 10})
    assert strategy.config["threshold"] == 10
    assert strategy.generate_signal() is True
