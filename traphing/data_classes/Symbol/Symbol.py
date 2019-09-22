# -*- coding: utf-8 -*-
import pandas as pd
from typing import List
from ... import utils
from ...utils import Timeframes

## Symbol methods written in other files
from . import core_functions as cf
from . import database_functions as dbf
from . import indicators as ind

class Symbol:
    def __init__(self, symbol_name: str, timeframes_list: List[Timeframes]):
        self.symbol_name = symbol_name
        self._velas_dict = dict()       #Internal dictionary with the available velas
        
        self.properties = SymbolProperties(symbol_name)
    
        self._create_velas(timeframes_list)
    
    @classmethod
    def load_symbols_info_from_csv( file_dir = "./storage/"):
        # This functions loads the symbol info file, and gets the
        # information about this symbol and puts it into the structure
        whole_path = file_dir + "Symbol_info.csv"
        try:
            infoCSV = pd.read_csv(whole_path,
                                  sep = ',')
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
    _create_velas = cf._create_velas
    add_velas = cf.add_velas
    del_velas = cf.del_velas
    set_time_interval =  cf.set_time_interval
    
    """
    Database methods
    """
    load_data_from_csv = dbf.load_data_from_csv
    add_data_from_csv = dbf.add_data_from_csv
    save_to_csv = dbf.save_to_csv
    update_csv = dbf.update_csv

class SymbolProperties:
    """ Class containing all the static information about a symbol"""
    def __init__(self, symbol_name):
        self.symbol_name = symbol_name 
        
        self.type = "Share"
        self.country = "Spain"
        self.currency = "EUR"
        self.sector = "Energy" 
        self.info = []
    
    def load_information_from_df(self, df):
        pass
        
    
