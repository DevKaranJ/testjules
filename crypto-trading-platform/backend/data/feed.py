class DataFeed:
    """
    Base class for market data feeds (live WebSockets or historical db).
    """

    def connect(self):
        pass

    def stream_data(self):
        """
        Stream data as MarketEvents.
        """
        pass
