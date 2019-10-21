import numpy as np
import pandas as pd

from .. import EntryStrategy, EntryTradeRequest
from .... import utils as ul

class CrossingMovingAverages(EntryStrategy):
    """This strategy is given 2 MAs and it will output a 1 if the lines are crossing
      We initialize it with the signals or with the portfolio and the shit.
    """
    def __init__(self, strategy_id, portfolio = None, slow_MA = None, fast_MA = None):
        super().__init__(strategy_id, portfolio)
        self.series_names = ["slow_MA", "fast_MA"]
        
        self.slow_MA = slow_MA
        self.fast_MA = fast_MA
        
    ### Specific elements of the strategy
    def set_slow_MA(self, signal_params): 
        self.slow_MA = signal_params
        
    def set_fast_MA(self, signal_params): 
        self.fast_MA = signal_params
    
    """
    ############ Overriding parent methods ###########################
    """
    def compute_input_series(self):
        slow_MA = self.portfolio.velas_indicator(**(self.slow_MA))
        fast_MA = self.portfolio.velas_indicator(**(self.fast_MA))
        series_df = pd.concat([slow_MA,fast_MA],axis =1, keys = self.series_names)
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
            symbol_name = self.fast_MA["symbol_name"]
            timeframe = self.fast_MA["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, price, action)

        return self.queue