import numpy as np
import pandas as pd

from .. import EntryStrategy
from ...exit import StopLoss
from ... import Trade
from .... import utils as ul
from ....data_classes import Portfolio

class CrossingMovingAverages(EntryStrategy):
    """Strategy: Given a fast and a slow Moving Average, fast_MA and slow_MA respectively:
        - If the fast_MA cross the slow_MA upwards: BUY trigger
        - If the fast_MA cross the slow_MA downwards: SELL trigger
    The slow_MA represents the baseline price and fast_MA the trend.
    
    Example of params:
        slow_MA_params = {"symbol_name":"AUDCHF","timeframe": Timeframes.M15,"indicator_name":"SMA", "args": {"n":45}}
        fast_MA_params = {"symbol_name":"AUDCHF","timeframe": Timeframes.M15,"indicator_name":"SMA", "args":{"n":20}}
        params = {"fast_MA": fast_MA_params, "slow_MA": slow_MA_params}
    """
    
    def __init__(self, name: str, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, portfolio, params)
        self.input_series_names = ["slow_MA", "fast_MA"]
    
    """
    ############ Overriding parent methods ###########################
    """
    def compute_input_series(self):
        slow_MA_params = self.params["slow_MA"]
        fast_MA_params = self.params["fast_MA"]
        slow_MA = self.portfolio.velas_indicator(**slow_MA_params)
        fast_MA = self.portfolio.velas_indicator(**fast_MA_params)
        series_df = pd.concat([slow_MA,fast_MA],axis = 1, keys = ["slow_MA", "fast_MA"])
        return series_df
    
    def compute_trigger_series(self):
        series_df = self.compute_input_series()
        trigger_series = ul.check_crossing(series_df["slow_MA"], series_df["fast_MA"])
        return trigger_series
        
    def compute_requests_queue(self):
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0)[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            action = self._get_action(trigger_series[indx])
            timestamp = trigger_series.index[indx]
            symbol_name = self.params["slow_MA"]["symbol_name"]
            timeframe = self.params["slow_MA"]["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, price, action)

        return self.queue
    
    def create_exit_strategy(self, trade: Trade):
        exit_strategy = StopLoss(name = "StopLoss_for_" + trade.name, trade = trade, portfolio = self.portfolio)
        
        symbol_name = trade.request.symbol_name
        timeframe = self.portfolio[trade.request.symbol_name].timeframes_list[0]
        exit_strategy.params["velas"] = {"symbol_name":symbol_name, "timeframe":timeframe}
        exit_strategy.set_stop_loss(pct = 0.3)
        return exit_strategy
        
