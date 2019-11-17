import numpy as np
import datetime as dt
import copy
import pandas as pd

from typing import List
from ... import utils
from ...utils import Timeframes
from ...data_classes import Symbol
from . import _indicators as ind

def _init_symbols(self, symbol_names: List[str], timeframes: List[Timeframes]):
    for symbol_name in symbol_names:
        self.add_symbol(symbol_name,timeframes)
                
#################### Getting and deleting symbols ###################
def add_symbol(self, symbol_name: str, timeframes: List[Timeframes] = None, symbol: Symbol = None):
    if symbol is None:
        symbol = Symbol(symbol_name, timeframes);
    elif timeframes is not None:
        symbol = Symbol.get_subsymbol(timeframes)
    else: 
        symbol = symbol
    self._symbols_dict[symbol_name] = symbol

def del_symbol(self, symbol_name: str):
    del self._symbols_dict[symbol_name] 

def del_all_symbols(self):
    self._symbols_dict = {}
    
def set_time_interval(self,start_time, end_time, trim = False):
    for symbol_name in self.symbol_names:
        self[symbol_name].set_time_interval(start_time, end_time, trim)
        
    self.start_time = start_time
    self.end_time = end_time
    
def load_symbols_properties_from_df(self, df):
    for symbol_name in self.symbol_names:
        self[symbol_name].load_properties_from_df(df)

def estimate_symbols_market_hours(self, timeframe = None):
    for symbol_name in self.symbol_names:
        self[symbol_name].estimate_market_hours(timeframe)

"""
####### velas interface 
"""

def velas_indicator(self, symbol_name, timeframe, indicator_name, args):
    return self[symbol_name][timeframe].indicator(indicator_name,**args)

def velas_series(self, symbol_name, timeframe, series_name, args):
    return self[symbol_name][timeframe].series(series_name,**args)

"""
####### others 
"""
def get_subportfolio(self, symbol_names = None, timeframes = None):
    """Returns a portfolio with only the desired symbols and timeframes
    """
    if symbol_names is None:
        symbol_names = self.symbol_names
        
    sub_portfolio = copy.copy(self)  #It only copies pointers
    sub_portfolio.del_all_symbols()
    
    for symbol_name in symbol_names:
        subsymbol = self[symbol_name].get_subsymbol(timeframes)
        sub_portfolio.add_symbol(symbol_name, symbol = subsymbol)
    
    return sub_portfolio


def map_timeframe(self, timeframe, method_name, *args, **kwargs):
    """It applies the given velas method to all of the porfolio velas of the given timeframe,
    with the given extra arguments. It returns the results as a pandas dataframe
    with the symbol_name as column names.
    """
    
    forex_intraday_close_values_pd = pd.concat([getattr(self[symbol_name][timeframe], method_name)(*args, **kwargs) for symbol_name in self.symbol_names],
                                                axis = 1, keys = self.symbol_names)
    return forex_intraday_close_values_pd

def indicator(self, name, *args, **kwargs):
    """
    Incators can use any candlestick in the data.
    """
    try:
        #method_func = getattr(self, method_name)
        indicator_func = getattr(ind, name)
    except AttributeError:
#        raise Warning("method_name: '%s' does not exist in the Velas object"%name)
        raise Warning("indicator_func: '%s' does not exist in the indicator library"%name)
#    kwargs["df"] = self.df ## TODO: Maybe this way is better in the future
    return indicator_func(self, *args, **kwargs)

"""
############################## GETTING LIST OF SUBSYMBOLS WITH SOME PROPERTIES 
"""

def get_related_forex_currencies(self, currency = None):
    """Returns a pd.Dataframe containing only the symbols that contain the given
    currency given as input.
    """
    new_symbol_names = []
    for symbol_name in self.symbol_names:
        if (symbol_name[:3] == currency ) | (symbol_name[3:] == currency ):
            new_symbol_names.append(symbol_name)
    symbol_names = new_symbol_names
    return symbol_names


def get_currencies_with_market_hours(self, open_time = dt.time(0), close_time = dt.time(0)):
    """It returns the symbol_names of the symbols which have the given
    open and close market hours
    """
    new_symbol_names = []
    for symbol_name in self.symbol_names:
        if self[symbol_name].market_hours.open_time != open_time:
            continue
        if self[symbol_name].market_hours.close_time != close_time:
            continue
        new_symbol_names.append(symbol_name)
    symbol_names = new_symbol_names
    return symbol_names

def get_non_empty(self, timeframe):
    """ Ir returns the symbol_names without the symbol_name of the symbols
    that do not have samples in the given time interval
    """
    new_symbol_names = []
    for symbol_name in self.symbol_names:
        if self[symbol_name][timeframe].timestamps.size == 0:
            continue
        new_symbol_names.append(symbol_name)
    symbol_names = new_symbol_names
    return symbol_names
