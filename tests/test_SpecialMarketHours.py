import sys
sys.path.append("..") # Adds higher directory to python modules path.
from traphing.data_classes import Velas
from traphing.utils import Timeframes, MarketHours, SpecialMarketHours
import traphing.utils as utils

import pytest
import datetime as dt
import pandas as pd
import numpy as np

class TestSpecialMarketHours():
    
    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        special_date = dt.date(year = 2019, month = 12, day = 25)
        my_special_market_hours = SpecialMarketHours(special_date)
        
        assert my_special_market_hours.date == special_date
        assert my_special_market_hours.open_time is None
        assert my_special_market_hours.close_time is None
        assert my_special_market_hours.n_samples is None
        
    def test_setting_data_externally(self):
        special_date = dt.date(year = 2019, month = 12, day = 25)
        open_time = dt.time(hour = 8, minute = 0, second = 0)
        close_time = dt.time(hour = 16, minute = 0, second = 0)
        n_samples = 60
        
        my_special_market_hours = SpecialMarketHours(special_date,open_time,close_time, n_samples)
        
        assert my_special_market_hours.date == special_date
        assert my_special_market_hours.open_time == open_time
        assert my_special_market_hours.close_time == close_time
        assert my_special_market_hours.n_samples == n_samples
        
    def test_is_non_trading_day(self):
        special_date = dt.date(year = 2019, month = 12, day = 25)
        open_time = dt.time(hour = 8, minute = 0, second = 0)
        close_time = dt.time(hour = 16, minute = 0, second = 0)
        n_samples = 60
        
        my_special_market_hours = SpecialMarketHours(special_date,open_time,close_time,n_samples)
        
        assert my_special_market_hours.is_non_trading_day() == False
        my_special_market_hours.n_samples = None
        assert my_special_market_hours.is_non_trading_day() == True
    
        
        