from queue import PriorityQueue
from ..utils import Actions
import pandas as pd
import datetime as dt
import numpy as np

class Strategy:
    """
    Parent class
    """
    def __init__(self, name, portfolio = None):
        self.name = name
        self.portfolio = portfolio
        
        self.requests_counter = 0  # Number of trading requests triggered
        self.queue = PriorityQueue() # Priority queue with the requests generated
        
    def _generate_new_request_name(self):
        name = str(self.name) + "#" + str(self.requests_counter)
        self.requests_counter += 1
        return name
	
    """
    Methods to be overriden by stratefy
    """
    def compute_input_series(self):
        """
        Compute the time series needed from the portfolio data.
        When calling this function, we assume that the porfolio has all the needed 
        data already.
        """
    def compute_trigger_series(self):
        """
        Computes the BULL-SELL triggers of the strategy
        # Mainly for visualization of the triggers
        """
    def compute_requests_queue(self):
        pass
    
    def compute_first_exit_request(self):
        queue = self.compute_requests_queue()
        if queue.empty() == False:
            return queue.get()
        else:
            return None

class TradeRequest:
    """
    This class is the one that characterizes the event of getting into the market
    Triggered by a certain class
    """
    def __init__(self, name: str, timestamp:pd.Timestamp, 
		symbol_name:str, price:float, action: Actions):
					 
        self.name = name          # id of the request
        self.strategy_name = self._get_strategy_name()  # ID of the the entry signal
        self.timestamp = timestamp   # Time when the signal was triggered
        
        # Identify the wanted trade
        self.symbol_name = symbol_name
        self.action = action  
        self.price = price
        
        # Variables related to the real world
        self.queue_timestamp = dt.datetime.now() # When it was actually generated
        
        # Additional information
        self.priority = 0            # Default priority
        self.comments = ""              # Comments for the trader
    
    def _get_strategy_name(self):
        return "#".join(list(np.array(self.name.split("#")[:-1])))
                               
    def __lt__(self, other):
        """
        Implemented because in the PriorityQueue, if it is the same, it will < the objects.
        With this, the newest object is always the lowest.
        """
        return True
  
class Trade:
    """
    Information class about a trade
    """
    def __init__(self, name, request, price):
        self.name = name
        self.request  = request  # Symbol of the Security (GLD, AAPL, IDX...)

        self.price = price
        self.timestamp = dt.datetime.now()
        
        self._copy_info_from_entry_signal()
        
    def _copy_info_from_entry_signal(self):
        self.action = self.request.action
        self.strategy_name = self.request.strategy_name
