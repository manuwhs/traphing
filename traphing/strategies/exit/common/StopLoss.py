import pandas as pd
import numpy as np
import datetime as dt

from .. import ExitStrategy, ExitTradeRequest
from .... import utils as ul

class StopLoss(ExitStrategy):
    """ 
    Exit the trade if it has lost X percent of its value.
    """

    def __init__(self, name, trade, portfolio = None, symbol_name = None, timeframe = None):
        super().__init__(name, trade, portfolio)
        self.series_names = ["Close","Stop_loss"]
        self.symbol_name = symbol_name
        self.timeframe = timeframe
        self.stop_loss = None
        

    def set_stop_loss(self, price = None, pct = None):
        """
        It sets the value of the stop loss
        """
        if price is not None:
            self.stop_loss = price
        else:
            sign = float(self.trade.action.value)*-1
            self.stop_loss = self.trade.price*(1 + sign*pct/100)
        
    def set_velas(self, symbol_name, timeframe):
        self.symbol_name = symbol_name
        self.timeframe = timeframe

    """
    ############ Overriding parent methods ###########################
    """
    
    def compute_input_series(self):
        close = self.portfolio[self.symbol_name][self.timeframe].series("Close")
        stop_loss = pd.Series(np.ones(close.index.size) * self.stop_loss, index = close.index)
        series_df = pd.concat([close,stop_loss],axis =1, keys = self.series_names)
        
        # Set to none the samples before the event
        series_df[series_df.index < self.trade.request.timestamp] = np.NaN
        return series_df
    
    
    def compute_trigger_series(self):
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["Stop_loss"],series_df["Close"])
        trigger_series = trigger_series.abs()
        return trigger_series

        
    def compute_requests_queue(self):
        # Creates the EntryTradingSignals for Backtesting
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0 )[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            timestamp = trigger_series.index[indx]
            symbol_name = self.symbol_name
            timeframe = self.timeframe
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, price)
        
        return self.queue
