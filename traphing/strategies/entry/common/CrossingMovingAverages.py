from queue import PriorityQueue
import numpy as np
import pandas as pd

from .. import EntryStrategy
from .... import utils as ul
from ....data_classes import Portfolio

class CrossingMovingAverages(EntryStrategy):
    """Strategy: Given a fast and a slow Moving Average, fast_MA and slow_MA respectively:
        - If the fast_MA crosses the slow_MA upwards: BUY trigger.
        - If the fast_MA crosses the slow_MA downwards: SELL trigger.
    The slow_MA represents the baseline price, and fast_MA represents the trend.
    
    Example of indicator params:
        slow_MA_params = {"symbol_name":"AUDCHF","timeframe": Timeframes.M15,"indicator_name":"SMA", "args": {"n":45}}
        fast_MA_params = {"symbol_name":"AUDCHF","timeframe": Timeframes.M15,"indicator_name":"SMA", "args":{"n":20}}
        indicators = {"fast_MA": fast_MA_params, "slow_MA": slow_MA_params}
    """
    
    def __init__(self, name: str, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, portfolio, params)

    def compute_input_series(self) -> pd.DataFrame:
        slow_MA_params = self.params["indicators"]["slow_MA"]
        fast_MA_params = self.params["indicators"]["fast_MA"]
        slow_MA = self.portfolio.velas_indicator(**slow_MA_params)
        fast_MA = self.portfolio.velas_indicator(**fast_MA_params)
        series_df = pd.concat([slow_MA,fast_MA],axis = 1, keys = ["slow_MA", "fast_MA"])
        return series_df
    
    def compute_trigger_series(self) -> pd.DataFrame:
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["slow_MA"], series_df["fast_MA"])
        pd.DataFrame(trigger_series, columns = [self.params["indicators"]["slow_MA"]["symbol_name"]])
        return trigger_series
        
    def compute_requests_queue(self) -> PriorityQueue:
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0)[0] 
        
        for indx in Event_indx:
            action = self._get_action(trigger_series[indx])
            timestamp = trigger_series.index[indx]
            symbol_name = self.params["indicators"]["slow_MA"]["symbol_name"]
            timeframe = self.params["indicators"]["slow_MA"]["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, timeframe, action, price)
        return self.queue
    