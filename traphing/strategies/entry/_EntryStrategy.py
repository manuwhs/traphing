import pandas as pd
import numpy as np
import datetime as dt
from queue import PriorityQueue

class EntryStrategy:
    """
    Class to generate trading signals. Template
    
    The end goal of a strategy is to generate TradeEvent signals
    """
    
    def __init__(self, strategy_id, portfolio = None):
        self.strategy_id = strategy_id
        self.portfolio = portfolio
        
        self.signal_params_list = None
        self.entry_requests_counter = 0  # Number of trading signals triggered

        self.queue = PriorityQueue()
        
    def set_signals(self):
        pass

    def compute_signals(self):
        pass
    
    def compute_entry_signals(self):
        pass
    
    def compute_entry_requests_queue(self):
        pass
