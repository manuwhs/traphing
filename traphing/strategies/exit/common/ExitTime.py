import pandas as pd
import numpy as np
import datetime as dt

from .. import ExitStrategy
from ... import Trade
from .... import utils as ul
from ....data_classes import Portfolio

class ExitTime(ExitStrategy):
    """Exit trade at the given time (every day).
    For example used to exit trades at the end of the day 
    """
    def __init__(self, name: str, trade: Trade, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, trade, portfolio, params)
        self.input_series_names = ["velas","time"]
        
    def compute_input_series(self) -> pd.DataFrame:
        symbol_name = self.params["velas"]["symbol_name"]
        timeframe = self.params["velas"]["timeframe"]
    
        velas = self.portfolio[symbol_name][timeframe]

        # substract timeframe because the timestamp in a candlestick is the beggining of the timeframe
        time_trigger = self.params["time"] #- dt.timedelta(minutes = velas.timeframe.value)
        time_trigger = ul.substract_times(time_trigger, dt.timedelta(minutes = velas.timeframe.value))
        
        series_df = pd.Series(np.zeros(velas.timestamps.size),index = velas.timestamps, name = "trigger_time")
        series_df[velas.timestamps.map(pd.Timestamp.time) == time_trigger] = 1
        
        # Set to none the samples before the event
        series_df[series_df.index < self.trade.request.timestamp] = 0
        series_df = pd.DataFrame(series_df)
        return series_df

    def compute_trigger_series(self) -> pd.Series:
        series_df = self.compute_input_series()
        trigger_series = series_df["trigger_time"]
        trigger_series = trigger_series.abs()
        trigger_series.name = "trigger_time_2"
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
