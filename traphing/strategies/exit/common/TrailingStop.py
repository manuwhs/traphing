import pandas as pd
import numpy as np

from .. import ExitStrategy
from ... import Trade
from .... import utils as ul
from .... utils import Actions
from ....data_classes import Portfolio

class TrailingStop(ExitStrategy):
    """Exit the trade if it has lost X percent of its value.
    """
    def __init__(self, name: str, trade: Trade, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, trade, portfolio, params)
        self.input_series_names = ["velas","stop_loss"]
        
    def compute_input_series(self) -> pd.DataFrame:
        symbol_name = self.params["velas"]["symbol_name"]
        timeframe = self.params["velas"]["timeframe"]
        pct = self.params["stop_loss"]["pct"]
        
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
            
        series_df = pd.concat([close,trailing_stop],axis =1, keys = self.input_series_names)
        return series_df
    
    def compute_trigger_series(self) -> pd.DataFrame:
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["stop_loss"],series_df["velas"])
        trigger_series = trigger_series.abs()
        return trigger_series

    def compute_requests_queue(self):
        # Creates the EntryTradingSignals for Backtesting
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0 )[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            timestamp = trigger_series.index[indx]
            symbol_name = self.params["velas"]["symbol_name"]
            timeframe = self.params["velas"]["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, price)
        
        return self.queue
