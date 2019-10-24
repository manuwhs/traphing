import pandas as pd
from .. import TradeRequest, Strategy 
from ...data_classes import Portfolio
from ...utils import Timeframes, get_empty_portfolio_params

class ExitTradeRequest(TradeRequest):
    """Contains the trade request information from an exit strategy.
    """
    def __init__(self, name, entry_trade, timestamp, symbol_name, timeframe, action, price):
        super().__init__(name, timestamp, symbol_name, timeframe, action, price)
        self.entry_trade = entry_trade

class ExitStrategy(Strategy):
    """Parent class to be inherited by all exit strategies. 
    The ultimate goal of this class is to generate exit trate requests and 
    place them in its internal priority queue.
    """

    @staticmethod
    def _include_request_velas_into_porfolio(trade, params):
        """Includes the velas parameters of the trade into the listening portfolio
        """
        try:
            params["portfolio"]
        except:
            params["portfolio"] = get_empty_portfolio_params()
            
        params["portfolio"]["symbol_names_list"].insert(0, trade.request.symbol_name)
        params["portfolio"]["timeframes_list"].insert(0, trade.request.timeframe)
        return params
    
    def __init__(self, name: str, trade: TradeRequest, portfolio: Portfolio = None,  params: dict = {}):
        self.trade = trade
        params = ExitStrategy._include_request_velas_into_porfolio(trade,params)
        super().__init__(name,portfolio, params)
    
    def create_request(self, timestamp: pd.Timestamp, symbol_name: str, timeframe: Timeframes, price: float):
        """Creates an EntryTradeRequest object and puts it in its queue.
        """
        name =  self._generate_new_request_name()
        trade = self.trade
        action = self.trade.request.action
        request =  ExitTradeRequest(name, trade, timestamp, symbol_name, timeframe, action, price)
        self.queue.put((request.timestamp, request))
    
    def compute_first_exit_request(self):
        queue = self.compute_requests_queue()
        if queue.empty() == False:
            return queue.get()
        else:
            return None
        
