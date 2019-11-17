# -*- coding: utf-8 -*-
import pandas as pd
from typing import List
from ... import utils
from ...utils import Timeframes
from ...data_classes import Symbol
## Symbol methods written in other files
from . import _core_functions as cf
from . import _database_functions as dbf
from . import _indicators as ind

class Portfolio:
    def __init__(self, portfolio_id: str, symbol_names: List[str], timeframes: List[Timeframes]):
        portfolio_id = portfolio_id
        self._symbols_dict = dict()
        # Loop over the symbol_names so loop over all the symbols in the Portfolio
        self._init_symbols(symbol_names, timeframes)  # Create the symbol objects from the periods and names

        ## Time constraining variables
        self.start_time = None  
        self.end_time = None
        
    @property
    def symbol_names(self):
        return list(self._symbols_dict.keys())

    @symbol_names.setter
    def symbol_names(self, value:  List[str]):
        ValueError("This property cannot be set externally")

    def __getitem__(self, key):
        val = self._symbols_dict[key]
        return val
    
    # secutities will be a dictionary of [symbol]

    _init_symbols = cf._init_symbols
    add_symbol = cf.add_symbol
    del_symbol = cf.del_symbol
    set_time_interval = cf.set_time_interval
    load_symbols_properties_from_df = cf.load_symbols_properties_from_df
    estimate_symbols_market_hours = cf.estimate_symbols_market_hours
    
    load_data_from_csv = dbf.load_data_from_csv
    add_data_from_csv = dbf.add_data_from_csv
    save_to_csv = dbf.save_to_csv
    update_csv = dbf.update_csv

    del_all_symbols = cf.del_all_symbols
    get_subportfolio = cf.get_subportfolio
    
    velas_indicator = cf.velas_indicator
    velas_series = cf.velas_series
    map_timeframe = cf.map_timeframe
    indicator = cf.indicator
    
    ## subselecting currencies
    get_related_forex_currencies = cf.get_related_forex_currencies
    get_currencies_with_market_hours = cf.get_currencies_with_market_hours
    get_non_empty = cf.get_non_empty
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


