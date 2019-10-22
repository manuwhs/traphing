import pandas as pd
from typing import Type

from .. import TradeRequest, Strategy
from ..exit import ExitStrategy
from ...utils import Actions
from ...data_classes import Portfolio

class EntryTradeRequest(TradeRequest):
    """Contains the trade request information from an entry strategy.
    """
    def __init__(self, name, timestamp, symbol_name, price , action):
        super().__init__(name, timestamp, symbol_name, price, action)
        
class EntryStrategy(Strategy):
    """Parent class to be inherited by all entry strategies. 
    The ultimate goal of this class is to generate entry trate requests and 
    place them in its internal priority queue.
    """
    
    def __init__(self, name: str, portfolio: Portfolio = None,  params: dict = {}):
        super().__init__(name,portfolio, params)        
    
    def _get_action(self, trigger_value: int):
        if (trigger_value == 1):
            action = Actions.BUY
        else:
            action = Actions.SELL
        return action
    
    def create_request(self, timestamp: pd.Timestamp, symbol_name: str, 
                       price: float, action: Actions):
        """Creates an EntryTradeRequest object and puts it in its queue.
        """
        name =  self._generate_new_request_name()
        request =  EntryTradeRequest(name, timestamp, symbol_name, price , action)
        self.queue.put((request.timestamp, request))
    
    """
    ################# Override ############################
    """
    
    def create_exit_strategy(self, trade: TradeRequest) -> Type[ExitStrategy]:
        """Creates a trading strategy from an entry trade
        If no specific strategy, return None.
        """
        return None