import pandas as pd
import numpy as np
import datetime as dt

from .. import TradeRequest, Strategy
from ...utils import Actions

class EntryTradeRequest(TradeRequest):
    """
    This class is the one that characterizes the event of getting into the market
    Triggered by a certain class
    """
    def __init__(self, name, timestamp, symbol_name, price , action):
        super().__init__(name, timestamp, symbol_name, price, action)
        
class EntryStrategy(Strategy):
    """
    Class to generate trading signals. Template
    
    The end goal of a strategy is to generate TradeEvent signals
    """
    
    def __init__(self, name, portfolio = None):
        super().__init__(name, portfolio)        
    
    def _get_action(self, trigger_value):
        if (trigger_value == 1):
            action = Actions.BUY
        else:
            action = Actions.SELL
        return action
    
    def create_request(self, timestamp, symbol_name, price, action):
        name =  self._generate_new_request_name()
        request =  EntryTradeRequest(name, timestamp, symbol_name, price , action)
        self.queue.put((request.timestamp, request))
            
