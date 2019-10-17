import pandas as pd
import numpy as np
import datetime as dt

class ExitStrategy:
    """
    Class to generate trading signals. Template
    
    The end goal of a strategy is to generate TradeEvent signals
    """
    
    def __init__(self, strategy_id, trade, portfolio = None):
        self.strategy_id = strategy_id
        self.portfolio = portfolio
        self.trade = trade
        
        self.signal_params_list = None
        self.exit_requests_counter = 0  # Number of trading signals triggered

        ## Related to the corresponding Entry Signal and 
        self.trade = trade
        
    def set_signals():
        """  It sets the hyperparameters 
        """
        pass

    def compute_signals():
        """ It computes them
        """
    
    def compute_exit_signals():
        """
        
        """
