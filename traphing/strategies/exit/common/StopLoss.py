import pandas as pd
import numpy as np

from .. import ExitStrategy
from ... import Trade
from .... import utils as ul
from ....data_classes import Portfolio

class StopLoss(ExitStrategy):
    """Exit the trade if it has lost X percent of its value.

    Example of indicator params:
        indicators = {"stop_loss_pct": 0.1}
    """
    def __init__(self, name: str, trade: Trade, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, trade, portfolio, params)
        self._set_stop_loss(**params["indicators"])
        
    def _set_stop_loss(self, stop_loss_price = None, stop_loss_pct = None):
        """
        It sets the value of the stop loss
        """
        if stop_loss_price is not None:
            stop_loss = stop_loss_price
        else:
            sign = float(self.trade.request.action.value)*-1
            stop_loss = self.trade.price*(1 + sign*stop_loss_pct/100)
            
        self.stop_loss = stop_loss
        
    def compute_input_series(self) -> pd.DataFrame:
        symbol_name = self.symbol_names[0]
        timeframe = self.timeframes[0]
        
        close = self.portfolio[symbol_name][timeframe].series("Close")
        stop_loss = pd.Series(np.ones(close.index.size) * self.stop_loss, index = close.index)
        series_df = pd.concat([close,stop_loss],axis =1, keys = ["close","stop_loss"])
        
        # Set to none the samples before the event
        series_df[series_df.index < self.trade.request.timestamp] = np.NaN
        return series_df
    
    def compute_trigger_series(self) -> pd.DataFrame:
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["stop_loss"],series_df["close"])
        trigger_series = trigger_series.abs()
        return trigger_series
        
    def compute_requests_queue(self):
        # Creates the EntryTradingSignals for Backtesting
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0 )[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            timestamp = trigger_series.index[indx]
            symbol_name = self.symbol_names[0]
            timeframe = self.timeframes[0]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, timeframe, price)
        
        return self.queue
