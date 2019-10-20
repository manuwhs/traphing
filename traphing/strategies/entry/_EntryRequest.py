import datetime as dt

class EntryRequest:
    """
    This class is the one that characterizes the event of getting into the market
    Triggered by a certain class
    """

    def __init__(self, entry_request_id, candlestick_timestamp, strategy_id, 
                 symbol_name, price, BUYSELL):
        # Identify the event !
        self.strategy_id = strategy_id          # ID of the strategy that generated the signal
        self.entry_request_id = entry_request_id  # ID of the the entry signal
        self.candlestick_timestamp = candlestick_timestamp           # Time when the signal was triggered
        
        # Identify the wanted trade
        self.symbol_name = symbol_name
        self.BUYSELL = BUYSELL  # Binary "BUY" or "SELL"
        self.price = price
        
        # Variables related
        self.signal_timestamp = dt.datetime.now() # When it was actually generated
        
        # Additional information
        self.priority = None          # Default priority
        self.recommendedPosition = None   # How much does the strategy recommend to buysell
        self.tradingStyle = None          # In which timeFrame are operating basically. Scalping, daytrading, long....
        
        self.comments = ""              # Comments for the trader
        
    def set_recommendations(self, priority = None, recommendedPosition = None,
                            tradingStyle = None):
        
        if(type(priority) != type(None)):
            self.priority = priority
        if(type(recommendedPosition) != type(None)):
            self.recommendedPosition = recommendedPosition
        if(type(priority) != type(None)):
            self.tradingStyle = tradingStyle


    def __lt__(self, other):
        """
        Implemented because in the PriorityQueue, if it is the same, it will < the objects.
        With this, the newest object is always the lowest.
        """
        return True