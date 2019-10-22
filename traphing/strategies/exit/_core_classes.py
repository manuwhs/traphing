import pandas as pd
from .. import TradeRequest, Strategy 
from ...data_classes import Portfolio

class ExitTradeRequest(TradeRequest):
    """Contains the trade request information from an exit strategy.
    """
    def __init__(self, name, entry_trade, timestamp, symbol_name, price , action):
        super().__init__(name, timestamp, symbol_name, price, action)
    
        self.entry_trade = entry_trade

class ExitStrategy(Strategy):
    """Parent class to be inherited by all exit strategies. 
    The ultimate goal of this class is to generate exit trate requests and 
    place them in its internal priority queue.
    """
    
    def __init__(self, name: str, trade: TradeRequest, portfolio: Portfolio = None,  params: dict = {}):
        super().__init__(name,portfolio,params)
        self.trade = trade

    def create_request(self, timestamp: pd.Timestamp, symbol_name: str, price: float):
        """Creates an EntryTradeRequest object and puts it in its queue.
        """
        name =  self._generate_new_request_name()
        trade = self.trade
        action = self.trade.request.action
        request =  ExitTradeRequest(name, trade, timestamp, symbol_name, price, action)
        self.queue.put((request.timestamp, request))
    
    def compute_first_exit_request(self):
        queue = self.compute_requests_queue()
        if queue.empty() == False:
            return queue.get()
        else:
            return None
        
