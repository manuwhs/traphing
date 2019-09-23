# -*- coding: utf-8 -*-
import pandas as pd
from typing import List
from ... import utils
from ...utils import Timeframes
from ...data_classes import Symbol
## Symbol methods written in other files
from . import core_functions as cf
from . import database_functions as dbf
from . import indicators as ind

class Portfolio:
    def __init__(self, portfolio_id: str, symbol_names_list: List[str], timeframes_list: List[Timeframes]):
        portfolio_id = portfolio_id
        self._symbols_dict = dict()
        # Loop over the symbol_names so loop over all the symbols in the Portfolio
        self._init_symbols(symbol_names_list, timeframes_list)  # Create the symbol objects from the periods and names
    
    
    @property
    def symbol_names_list(self):
        return list(self._symbols_dict.keys())

    @symbol_names_list.setter
    def symbol_names_list(self, value:  List[str]):
        ValueError("This property cannot be set externally")

    def __getitem__(self, key):
        val = self._symbols_dict[key]
        return val
    
    # secutities will be a dictionary of [symbol]

    _init_symbols = cf._init_symbols
    add_symbol = cf.add_symbol
    del_symbol = cf.del_symbol
    set_time_interval = cf.set_time_interval

    get_timeSeries = cf.get_timeSeries
    get_timeSeriesReturn = cf.get_timeSeriesReturn
    get_timeSeriesCumReturn = cf.get_timeSeriesCumReturn
    

    load_data_from_csv = dbf.load_data_from_csv
    add_data_from_csv = dbf.add_data_from_csv
    save_to_csv = dbf.save_to_csv
    update_csv = dbf.update_csv


    #######################################################################
    #### DDBB Operations ##################################################
    #######################################################################
if(0):

    #######################################################################
    #### Operations over all the prices of the portfolio ##################
    #######################################################################

    get_daily_symbolsPrice = CPop.get_daily_symbolsPrice
    plot_daily_symbolsPrice = CPop.plot_daily_symbolsPrice
    get_daily_symbolsCumReturn = CPop.get_daily_symbolsCumReturn
    
    get_intra_by_days = CPin.get_intra_by_days


