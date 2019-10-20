import numpy as np
import pandas as pd

from .. import EntryStrategy, EntryRequest
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
    
    def compute_strategy_series(self):
        """
        Function that computes the signals
        """
        slow_MA = self.portfolio.velas_indicator(**(self.slow_MA))
        fast_MA = self.portfolio.velas_indicator(**(self.fast_MA))
        
        series = pd.concat([slow_MA,fast_MA],axis =1, keys = self.series_names)
        return series
    
    #### BackTesting functions #######
    def compute_entry_series(self):
        """
        Computes the BULL-SELL triggers of the strategy
        # Mainly for visualization of the triggers
        """
        signals = self.compute_strategy_series()
        crosses = ul.check_crossing(signals["slow_MA"], signals["fast_MA"])
        return crosses
        
    def compute_entry_requests_queue(self):
        """
        Returns a dictionary with the Entry signals
        """
        crosses = self.compute_entry_series()
        Event_indx = np.where(crosses != 0)[0] # We do not care about the second dimension
        for indx in Event_indx:
            if (crosses[indx] == 1):
                BUYSELL = "BUY"
            else:
                BUYSELL = "SELL"
            
            candlestick_timestamp = crosses.index[indx]
            symbol_name = self.fast_MA["symbol_name"]; timeframe = self.fast_MA["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(candlestick_timestamp)["Close"])
            # Create the trading sigal !
            entry_request =  EntryRequest(entry_request_id = str(self.entry_requests_counter), 
                                       strategy_id = self.strategy_id, 
                                       candlestick_timestamp = candlestick_timestamp,
                                       BUYSELL = BUYSELL, price = price, symbol_name = symbol_name)
            
            entry_request.comments = "Basic Crossing MA man !"
            entry_request.priority = 0
            entry_request.recommendedPosition = 1 
            entry_request.tradingStyle = "dayTrading"
            
            self.queue.put((crosses.index[indx], entry_request))
            self.entry_requests_counter += 1
        return self.queue