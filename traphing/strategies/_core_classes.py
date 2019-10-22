from queue import PriorityQueue
from ..utils import Actions
from ..data_classes import Portfolio

import pandas as pd
import datetime as dt
import numpy as np
from typing import Type

class Strategy:
    """Parent class for trading strategies.
    """
    def __init__(self, name: str, portfolio: Portfolio = None, params: dict = {}):
        self.name = name
        self.params = params

        self.portfolio = portfolio
        
        self.requests_counter = 0       # Number of trading requests triggered
        self.queue = PriorityQueue()    # Priority queue with the requests generated
        
    def _generate_new_request_name(self) -> str:
        """Generates a new request name so that all of them have unique ids
        """
        name = str(self.name) + "#" + str(self.requests_counter)
        self.requests_counter += 1
        return name
	
    def set_params(self, params: dict):
        self.params = params
        self.input_series_names = list(params.keys())
        
    """
    Methods to be overriden.
    """
    def compute_input_series(self) -> pd.DataFrame:
        """Computes the time series needed from the candlesticks in the portfolio.
        When calling this function, we assume that the porfolio has all the needed 
        data already and its time interval has been d
        """
    def compute_trigger_series(self) -> pd.DataFrame:
        """Computes the triggers of the strategy in a time series where most
        elements will be 0. The rest of the element will be:
            - 1: For a BUY trigger. (or for clossing a trade if it is an exit strategy)
            - -1: For a SELL trigger.
        It should call the compute_input_series() method and use its time series.
        to compute the final triggers. 
        """
    def compute_requests_queue(self) -> pd.DataFrame:
        """Computes the trade requests objects and puts them into the queue.
        It should call the compute_trigger_series() method to get the time series
        of triggers and then handle each of them to create the requests.
        """

    def plot_strategy(self, axes_input, axes_triggers):
        """This function plots the strategies series and its triggers.
        It might not be useful for all cases but it is a nice initial approximation
        """
        
class TradeRequest:
    """
    Parent class for the trade requests objects. It contains the information of
    the requested trade by a strategy.
    """
    def __init__(self, name: str, timestamp: pd.Timestamp, 
		symbol_name: str, price: float, action: Actions):
					 
        self.name = name          
        self.strategy_name = self._get_strategy_name() 
        self.timestamp = timestamp   
        
        # Identify the wanted trade
        self.symbol_name = symbol_name
        self.action = action  
        self.price = price
        
        # Variables related to the real world
        self.queue_timestamp = dt.datetime.now() # When it was actually generated
        
        # Additional information
        self.priority = 0               # Default priority
        self.comments = ""              # Comments for the trader
    
    def _get_strategy_name(self) -> str:
        return "#".join(list(np.array(self.name.split("#")[:-1])))
                               
    def __lt__(self, other):
        """Overrding of "<" because in the PriorityQueue, 
        if we have 2 elements with the same timestamp it will compare the objects using "<".
        With this function, the last element to be added will be put last.
        """
        return True
  

class Trade:
    """Information class about a performed trade. It contains the information regarding
    a performed trade. It keeps the accepted request as an attribute.
    """
    def __init__(self, name: str, request: Type[TradeRequest], price: float):
        self.name = name
        self.request  = request  # Symbol of the Security (GLD, AAPL, IDX...)

        self.price = price
        self.timestamp = dt.datetime.now()
        