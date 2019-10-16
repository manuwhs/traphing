import pandas as pd
import numpy as np
import datetime as dt

class EntryStrategy:
    """
    Class to generate trading signals. Template
    
    The end goal of a strategy is to generate TradeEvent signals
    """
    
    def __init__(self, strategy_id, portfolio = None):
        self.strategy_id = strategy_id
        self.portfolio = portfolio
        
        self.signal_params_list = None
        self.entry_signals_counter = 0  # Number of trading signals triggered

        
    def set_signals():
        """  It sets the hyperparameters 
        """
        pass

    def compute_signals():
        """ It computes them
        """
    
    def compute_entry_signals():
        """
        
        """
