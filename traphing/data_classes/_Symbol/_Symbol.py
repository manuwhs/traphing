# -*- coding: utf-8 -*-
import pandas as pd
from typing import List
from ... import utils
from ...utils import Timeframes, MarketHours

## Symbol methods written in other files
from . import _core_functions as cf
from . import _database_functions as dbf
from . import _indicators as ind

class Symbol:
    def __init__(self, symbol_name: str, timeframes_list: List[Timeframes], 
                 symbol_properties_df: pd.DataFrame = None):
        self.symbol_name = symbol_name
        self._velas_dict = dict()       #Internal dictionary with the available velas
        
        self.properties = SymbolProperties(symbol_name, symbol_properties_df)
        self.market_hours = MarketHours()
        
        self._init_velas(timeframes_list)
    
    @classmethod
    def load_symbols_properties_csv(cls, file_dir: str):
        """ This function load the csv file that contains the properties
        of all symbols in the broker 
        """
        whole_path = file_dir + "symbols_properties.csv"
        try:
            infoCSV = pd.read_csv(whole_path,
                                  sep = ',', index_col = "symbol_name")
        except IOError:
            error_msg = "Empty file: " + whole_path 
            print (error_msg)
        
        return infoCSV
    
    @classmethod
    def save_symbols_properties_to_csv(cls, file_dir: str, df: pd.DataFrame):
        whole_path = file_dir + "symbols_properties.csv"
        try:
            infoCSV = df.to_csv(whole_path)
        except IOError:
            error_msg = "Empty file: " + whole_path 
            print (error_msg)
        
        return infoCSV

    @property
    def timeframes_list(self):
        return list(self._velas_dict.keys())

    @timeframes_list.setter
    def timeframes_list(self, value:  List[Timeframes]):
        ValueError("This property cannot be set externally")

    def __getitem__(self, key):
        val = self._velas_dict[key]
        return val
    
    """
    Core methods
    """
    _init_velas = cf._init_velas
    add_velas = cf.add_velas
    del_velas = cf.del_velas
    set_time_interval =  cf.set_time_interval
    load_properties_from_df = cf.load_properties_from_df
    estimate_market_hours = cf.estimate_market_hours
    """
    Database methods
    """
    load_data_from_csv = dbf.load_data_from_csv
    add_data_from_csv = dbf.add_data_from_csv
    save_to_csv = dbf.save_to_csv
    update_csv = dbf.update_csv

class SymbolProperties:
    """ Class containing all the static information about a symbol"""
    def __init__(self, symbol_name, df = None):
        self.symbol_name = symbol_name 
        
        self.type = None
        self.country = None
        self.currency = None
        self.sector = None 
        
        self.contract_size = None
        self.point_size = None
        self.min_tick_value = None
    
        if df is not None:
            self.set_properties_from_df(df)
            
    def load_properties_from_df(self, df):
        df = df.loc[self.symbol_name]
        self.contract_size = float(df["contract_size"])
        self.point_size = float(df["point_size"])
        self.min_tick_value = float(df["min_tick_value"])
        
        self.currency = df["currency"]
        

