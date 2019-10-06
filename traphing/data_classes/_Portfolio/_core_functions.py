# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 03:04:26 2016

@author: montoya
"""


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


def get_timeSeries(self, symbolIDs = [], period = None, seriesNames = []):
    # This funciton returns a list with the timeSeries for all of the
    # symbols specified, for a given period.

    symbolIDs, period = self.default_select(symbolIDs, period)
    all_timeSeries = []

    for symbol_n in symbolIDs:
        timeSeries = self.symbols[symbol_n].timeDatas[period].get_timeSeries(seriesNames = seriesNames);
        all_timeSeries.append(timeSeries)
    return all_timeSeries

def get_timeSeriesReturn(self, symbolIDs = [], period = None, seriesNames = []):
    # This funciton returns a list with the timeSeries for all of the
    # symbols specified, for a given period.

    symbolIDs, period = self.default_select(symbolIDs, period)
    all_timeSeries = []
    for symbol_n in symbolIDs:
        timeSeries = self.symbols[symbol_n].timeDatas[period].get_timeSeriesReturn(seriesNames = seriesNames);
        all_timeSeries.append(timeSeries)
    return all_timeSeries
    
def get_timeSeriesCumReturn(self, symbolIDs = [], period = None, seriesNames = []):
    # This funciton returns a list with the timeSeries for all of the
    # symbols specified, for a given period.

    symbolIDs, period = self.default_select(symbolIDs, period)
    all_timeSeries = []
    for symbol_n in symbolIDs:
        timeSeries = self.symbols[symbol_n].timeDatas[period].get_timeSeriesCumReturn(seriesNames = seriesNames);
        all_timeSeries.append(timeSeries)
    return all_timeSeries

