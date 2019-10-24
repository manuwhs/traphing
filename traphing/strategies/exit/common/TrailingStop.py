import pandas as pd
import numpy as np

from .. import ExitStrategy
from ... import Trade
from .... import utils as ul
from .... utils import Actions
from ....data_classes import Portfolio

class TrailingStop(ExitStrategy):
    """Exit the trade if it has lost X percent of its value.
    
    Example of indicator params:
        indicators = {"stop_loss_pct": 0.1}
    """
    def __init__(self, name: str, trade: Trade, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, trade, portfolio, params)

    def compute_input_series(self) -> pd.DataFrame:
        symbol_name = self.symbol_names_list[0]
        timeframe = self.timeframes_list[0]
        pct = self.params["indicators"]["stop_loss_pct"]
        
        close = self.portfolio[symbol_name][timeframe].series("Close")
        
        # Compute the trailing stop
        sign = float(self.trade.request.action.value)*-1
        close_pct_threshold = close*(1 + sign*pct/100)

        # Set to none the samples before the event
        close_pct_threshold[close.index < self.trade.request.timestamp] = np.NaN
        
        if self.trade.request.action == Actions.BUY:
            trailing_stop = close_pct_threshold.cummax()
        elif self.trade.request.action == Actions.SELL: 
            trailing_stop = close_pct_threshold.cummin()
            
        series_df = pd.concat([close,trailing_stop],axis =1, keys = ["close_values","trailing_stop"])
        return series_df
    
    def compute_trigger_series(self) -> pd.DataFrame:
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["trailing_stop"],series_df["close_values"])
        trigger_series = trigger_series.abs()
        return trigger_series

    def compute_requests_queue(self):
        # Creates the EntryTradingSignals for Backtesting
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0 )[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            timestamp = trigger_series.index[indx]
            symbol_name = self.symbol_names_list[0]
            timeframe = self.timeframes_list[0]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, timeframe, price)
        
        return self.queue
