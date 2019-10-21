import pandas as pd
import numpy as np
import datetime as dt

from .. import TradeRequest, Strategy 

class ExitTradeRequest(TradeRequest):
    """
    This class is the one that characterizes the event of getting into the market
    Triggered by a certain class
    """
    def __init__(self, name, entry_trade, timestamp, symbol_name, price , action):
        super().__init__(name, timestamp, symbol_name, price, action)
    
        self.entry_trade = entry_trade

class ExitStrategy(Strategy):
    """
    Class to generate trading signals. Template
    The end goal of a strategy is to generate TradeEvent signals
    """
    
    def __init__(self, name, trade, portfolio = None):
        super().__init__(name, portfolio)
        self.trade = trade

    def create_request(self, timestamp, symbol_name, price):
        name =  self._generate_new_request_name()
        trade = self.trade
        action = self.trade.request.action
        request =  ExitTradeRequest(name, trade, timestamp, symbol_name, price, action)
        self.queue.put((request.timestamp, request))
        
