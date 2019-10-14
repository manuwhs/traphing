import sys
sys.path.insert(0,"..") # Adds higher directory to python modules path.
from traphing.data_classes import Symbol
from traphing.utils import Timeframes
import pytest
import datetime as dt
import pandas as pd

# @pytest.fixture
def get_loaded_Symbol():
    symbol_name = "AUDCHF"
    timeframes_list = [Timeframes.M15, Timeframes.D1]
    storage_folder = "./data/storage/"
    
    my_symbol = Symbol(symbol_name, timeframes_list)
    my_symbol.load_data_from_csv(storage_folder)
    
    return my_symbol
    
    
class TestSymbol():
    
    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        symbol_name = "AUDCHF"
        timeframes_list = [Timeframes.M15, Timeframes.D1]
        
        my_symbol = Symbol(symbol_name, timeframes_list)
        
        assert symbol_name == my_symbol.symbol_name
        assert timeframes_list == my_symbol.timeframes_list

    def test_add_del_velas(self):
        """ Basic initialization parameters 
        """
        symbol_name = "AUDCHF"
        timeframes_list = [Timeframes.M15, Timeframes.D1]
        
        my_symbol = Symbol(symbol_name, timeframes_list)
        my_symbol.add_velas(Timeframes.M5)
        assert my_symbol.timeframes_list == [Timeframes.M15, Timeframes.D1, Timeframes.M5]
        
        my_symbol.del_velas(Timeframes.M5)
        my_symbol.del_velas(Timeframes.M15)
        assert my_symbol.timeframes_list == [Timeframes.D1]
        
        my_symbol.add_velas(Timeframes.M15)
        assert my_symbol.timeframes_list == [Timeframes.D1, Timeframes.M15]
    
    def test__get_item__(self):
        symbol_name = "AUDCHF"
        timeframes_list = [Timeframes.M15, Timeframes.D1]
        my_symbol = Symbol(symbol_name, timeframes_list)
        assert my_symbol[Timeframes.M15] == my_symbol._velas_dict[Timeframes.M15]
        
    def test_load_data_from_csv(self):
        my_symbol = get_loaded_Symbol()
        assert my_symbol[Timeframes.M15].df.shape == (100400,5)
        assert my_symbol[Timeframes.D1].df.shape  == (4894,5)

    def test_set_time_interval_complex(self):
        """ We test several succesive scenarios"""
        
        start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
        my_symbol = get_loaded_Symbol()
        
        my_symbol.set_time_interval(start_time, end_time, trim = False)
        
        assert my_symbol[Timeframes.M15].df.shape == (2112,5)
        assert my_symbol[Timeframes.M15]._df.shape == (100400,5)
        assert my_symbol[Timeframes.M15].timestamps.shape == (2112,)

        assert my_symbol[Timeframes.D1].df.shape == (22,5)
        assert my_symbol[Timeframes.D1]._df.shape == (4894,5)
        assert my_symbol[Timeframes.D1].timestamps.shape == (22,)
        
        
        
        
        
