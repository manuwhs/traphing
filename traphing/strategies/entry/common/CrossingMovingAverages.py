import numpy as np
import pandas as pd

from .. import EntryStrategy, EntrySignal
from .... import utils as ul

class CrossingMovingAverages(EntryStrategy):
    """This strategy is given 2 MAs and it will output a 1 if the lines are crossing
      We initialize it with the signals or with the portfolio and the shit.
    """
    def __init__(self, strategy_id, portfolio = None, slow_MA = None, fast_MA = None):
        super().__init__(strategy_id, portfolio)
        self.signal_names = ["slow_MA", "fast_MA"]
        
        self.slow_MA = slow_MA
        self.fast_MA = fast_MA
        
    ### Specific elements of the strategy
    def set_slow_MA(self, signal_params): 
        self.slow_MA = signal_params
        
    def set_fast_MA(self, signal_params): 
        self.fast_MA = signal_params
    
    def compute_signals(self):
        """
        Function that computes the signals
        """
        slow_MA = self.portfolio.velas_indicator(**(self.slow_MA))
        fast_MA = self.portfolio.velas_indicator(**(self.fast_MA))
        
        signals = pd.concat([slow_MA,fast_MA],axis =1, keys = self.signal_names)
        return signals
    
    #### BackTesting functions #######
    def compute_entry_signals(self):
        """
        Computes the BULL-SELL triggers of the strategy
        # Mainly for visualization of the triggers
        """
        signals = self.compute_signals()
        crosses = ul.check_crossing(**signals)
        return crosses
        
    def get_entry_signals_dict(self):
        """
        Returns a dictionary with the Entry signals
        """
        entry_signals_dict = {}
        crosses = self.compute_entry_signals()
        Event_indx = np.where(crosses != 0) # We do not care about the second dimension
        for indx in Event_indx[0]:
            if (crosses[indx] == 1):
                BUYSELL = "BUY"
            else:
                BUYSELL = "SELL"
            # Create the trading sigal !
            entry_signal =  EntrySignal( timestamp = crosses.index[indx], 
                                       entry_signal_id = str(self.entry_signals_counter), 
                                       strategy_id = self.strategy_id, 
                                       BUYSELL = BUYSELL)
            
            entry_signal.comments = "Basic Crossing MA man !"
            entry_signal.priority = 0
            entry_signal.recommendedPosition = 1 
            entry_signal.tradingStyle = "dayTrading"
            
            entry_signals_dict[crosses.index[indx]] = entry_signal
            self.entry_signals_counter += 1
        return entry_signals_dict