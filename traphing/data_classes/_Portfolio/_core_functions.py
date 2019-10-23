import numpy as np
import datetime as dt

from typing import List
from ... import utils
from ...utils import Timeframes
from ...data_classes import Symbol

#################### Getting and deleting periods ###################
def _init_symbols(self, symbol_names_list: List[str], timeframes_list: List[Timeframes]):
    for symbol_name in symbol_names_list:
        self.add_symbol(symbol_name,timeframes_list)
                
#################### Getting and deleting symbols ###################
# Symbols will be a dictionary of [symbol]
# We will access them from the outside with these functions
def add_symbol(self, symbol_name: str, timeframes_list: List[Timeframes], symbol: Symbol = None):
    # Sets the secutities list
    if (symbol is None):
        symbol = Symbol(symbol_name, timeframes_list);
    self._symbols_dict[symbol_name] = symbol

def del_symbol(self, symbol_name: str):
    # This function deletes the timeData object to the Symbol.
    del self._symbols_dict[symbol_name] 

def set_time_interval(self,start_time, end_time, trim = False):
    for symbol_name in self.symbol_names_list:
        self[symbol_name].set_time_interval(start_time, end_time, trim)
        
    self.start_time = start_time
    self.end_time = end_time
    
def load_symbols_properties_from_df(self, df):
    for symbol_name in self.symbol_names_list:
        self[symbol_name].load_properties_from_df(df)

def estimate_symbols_market_hours(self, timeframe = None):
    for symbol_name in self.symbol_names_list:
        self[symbol_name].estimate_market_hours(timeframe)
        
"""

"""

def velas_indicator(self, symbol_name, timeframe, indicator_name, args):
    return self[symbol_name][timeframe].indicator(indicator_name,**args)
