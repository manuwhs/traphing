import sys
sys.path.append("..") # Adds higher directory to python modules path.
import traphing.data_classes.Velas as Velas
from traphing.utils import Timeframes
import pytest
import datetime as dt
import pandas as pd
import numpy as np

# @pytest.fixture
def get_loaded_Vela():
    symbol_name = "AUDCHF"
    timeframe = Timeframes.M15
    storage_folder = "./data/storage/"
    
    my_vela = Velas(symbol_name, timeframe)
    my_vela.load_data_from_csv(storage_folder)
    
    return my_vela
    
    
class TestVelasIndicators():
    
    def test_SMA(self):
        start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
        my_vela = get_loaded_Vela()
        
        my_vela.set_time_interval(start_time, end_time)
        
        n = 10
        my_SMA = my_vela.SMA(n = n)
        
        assert my_SMA.shape == (2112,)
        assert isinstance(my_SMA, pd.Series)
        assert np.mean(np.isnan(my_SMA.values[:n-1])) == 1
        assert np.mean(np.isnan(my_SMA.values[n:])) == 0

my_test = TestVelasIndicators()
my_test.test_SMA()