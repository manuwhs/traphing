import sys
sys.path.append("..") # Adds higher directory to python modules path.
import traphing.data_classes.Velas as Velas
import pytest
import datetime as dt
import pandas as pd

# @pytest.fixture
def get_loaded_Vela():
    symbol_name = "AUDCHF"
    timeframe = 15
    storage_folder = "./data/storage/"
    
    my_vela = Velas(symbol_name, timeframe)
    my_vela.load_data_from_csv(storage_folder)
    
    return my_vela
    
    
class TestVelas():
    
    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        symbol_name = "AUDCHF"
        timeframe = 15
        
        my_vela = Velas(symbol_name, timeframe)
        
        assert symbol_name == my_vela.symbol_name
        assert timeframe == timeframe
    
    def test_load_data_from_csv(self):
        my_vela = get_loaded_Vela()
        assert my_vela.df.shape == (100400,5)
        assert my_vela.dates.shape == (100400,)
        assert isinstance(my_vela.dates,pd.DatetimeIndex)
        assert isinstance(my_vela.df,pd.DataFrame) 
    
    def test_set_time_interval_trimming(self):
        start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
        my_vela = get_loaded_Vela()
        
        my_vela.set_time_interval(start_time, end_time)
        
        assert my_vela.df.shape == (2112,5)
        assert my_vela._df.shape == (2112,5)
        assert my_vela.dates.shape == (2112,)

    def test_set_time_interval_no_trimming(self):
        start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
        my_vela = get_loaded_Vela()
        
        my_vela.set_time_interval(start_time, end_time, trim = False)
        
        assert my_vela.df.shape == (2112,5)
        assert my_vela._df.shape == (100400,5)
        assert my_vela.dates.shape == (2112,)
    
    def test_set_time_interval_complex(self):
        """ We test several succesive scenarios"""
        
        start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
        my_vela = get_loaded_Vela()
        
        my_vela.set_time_interval(start_time, end_time, trim = False)
        
        assert my_vela.df.shape == (2112,5)
        assert my_vela._df.shape == (100400,5)
        assert my_vela.dates.shape == (2112,)
        
    def test_save_to_csv(self):
        my_vela = get_loaded_Vela()
        storage_folder = "./data/storage2/"
        my_vela.save_to_csv(storage_folder)
        
        nueva_vela = Velas(my_vela.symbol_name, my_vela.timeframe)
        nueva_vela.load_data_from_csv(storage_folder)
        assert my_vela._df.shape == nueva_vela._df.shape
    
    def test_add_data_from_csv(self):
        symbol_name = "AUDCAD"
        timeframe = 15
        storage_folder = "./data/storage/"
        storage2_folder = "./data/storage2/"
        
        my_vela = Velas(symbol_name, timeframe)
        my_vela2 = Velas(symbol_name, timeframe)
        
        my_vela.load_data_from_csv(storage_folder)
        my_vela2.load_data_from_csv(storage2_folder)
        
        assert my_vela._df.shape == (99483,5)
        assert my_vela2._df.shape == (38208,5)
        
        my_vela.add_data_from_csv(storage2_folder)
    
        assert my_vela._df.shape == (100400,5)
        
    def test_get_series(self):
        options = ["Open","Close","High","Low","Volume","Average", "RangeHL","RangeCO"]
        
        my_vela = get_loaded_Vela()
        
        for name in options:
            time_series_data = my_vela.series(name)
            
            assert time_series_data.shape == (my_vela.df.shape[0],)
            assert isinstance(time_series_data, pd.Series)
        
        