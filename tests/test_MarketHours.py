import sys
sys.path.insert(0,"..") # Adds higher directory to python modules path.
from traphing.data_classes import Velas
from traphing.utils import Timeframes, MarketHours, SpecialMarketHours
import traphing.utils as utils

import pytest
import datetime as dt
import pandas as pd
import numpy as np

# @pytest.fixture
def get_loaded_Velas():
    symbol_name = "AUDCHF"
    timeframe = Timeframes.M15
    storage_folder = "../tests/data/storage/"
    start_time = dt.datetime(2019,7,20)
    end_time = dt.datetime(2019,8,20)
    
    my_velas_M15 = Velas(symbol_name, timeframe)
    my_velas_M15.load_data_from_csv(storage_folder)
    my_velas_M15.set_time_interval(start_time, end_time, trim = False)
    
    return my_velas_M15
    
def get_loaded_market_hours():
    open_time = dt.time(hour = 8, minute = 0, second = 0)
    close_time = dt.time(hour = 16, minute = 0, second = 0)
    trading_days_list =  [0, 1, 2, 3 ,4] # Weekdays
    special_date = dt.date(year = 2019, month = 12, day = 25)
    special_market_hours = SpecialMarketHours(special_date, open_time = dt.time(9,0,0),close_time = dt.time(14,0,0))
    special_days_dict = {special_market_hours.date: special_market_hours}
    my_market_hours = MarketHours(open_time, close_time, trading_days_list, special_days_dict = special_days_dict)
    return my_market_hours
    
class TestMarketHours():
    
    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        my_market_hours = MarketHours()
        
        assert my_market_hours.open_time is None
        assert my_market_hours.close_time is None
        assert my_market_hours.trading_days_list is None
        assert my_market_hours.special_days_dict is None
        
    def test_setting_data_externally(self):
        open_time = dt.time(hour = 8, minute = 0, second = 0)
        close_time = dt.time(hour = 16, minute = 0, second = 0)
        trading_days_list =  [0, 1, 2, 3 ,4] # Weekdays
        
        my_market_hours = MarketHours(open_time,close_time, trading_days_list)
        
        assert my_market_hours.open_time == open_time
        assert my_market_hours.close_time == close_time
        assert my_market_hours.trading_days_list == trading_days_list
        
    def test_setting_special_days_dict(self):
        special_date = dt.date(year = 2019, month = 12, day = 25)
        special_market_hours = SpecialMarketHours(special_date, open_time = dt.time(9,0,0))
        special_days_dict = {special_market_hours.date: special_market_hours}
        
        my_market_hours = MarketHours(special_days_dict = special_days_dict)
        assert my_market_hours.special_days_dict == special_days_dict
    
    def test_date_related_chechings(self):
        my_market_hours = get_loaded_market_hours()
        date = dt.date(2019,10,2)
        
        assert my_market_hours.is_trading_day(date) == True
        assert my_market_hours.is_special(date) == False 
        assert my_market_hours.should_be_usual_trading_day(date) == True
        
    def test_datetime_related_chekings(self):
        my_market_hours = get_loaded_market_hours()
        datetime_1 = dt.datetime(2019,10,2, 7,0, 0)
        datetime_2 = dt.datetime(2019,10,2, 15,0, 0)
        special_date = list(my_market_hours.special_days_dict.keys())[0]
        special_datetime = dt.datetime(special_date.year,special_date.month,special_date.day, 15,0, 0)
        
        assert my_market_hours.is_market_open(datetime_1) == False
        assert my_market_hours.is_market_open(datetime_2) == True
        assert my_market_hours.is_market_open(special_datetime) == False
    
    def test_other_trading_session_info(self):
        my_market_hours = get_loaded_market_hours()
        datetime_1 = dt.datetime(2019,10,2, 7,0, 0)
        special_date = list(my_market_hours.special_days_dict.keys())[0]

        assert my_market_hours.get_length_session_in_seconds(datetime_1.date()) == (28800, 57600)
        assert my_market_hours.get_length_session_in_seconds(special_date) == (18000, 68400)
        assert my_market_hours.get_number_of_samples_of_trading_session(Timeframes.M15, datetime_1.date()) == 32
        assert my_market_hours.get_number_of_samples_of_trading_session(Timeframes.M15, special_date) == 20
        

    def test_estimate_timeframe(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        timestamps_M15 = my_velas_M15.timestamps
        assert my_market_hours.estimate_timeframe(timestamps_M15) == Timeframes.M15

    def test_estimate_open_close_time(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        timestamps_M15 = my_velas_M15.timestamps
        time_0 = dt.time(0,0,0)
        assert my_market_hours.estimate_open_close_time(timestamps_M15) == (time_0,time_0)

    def test_estimate_normal_trading_days(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        timestamps_M15 = my_velas_M15.timestamps
        days_list = [0,1,2,3,4]
        assert my_market_hours.estimate_normal_trading_days(timestamps_M15) == days_list
        
    def test_estimate_special_trading_days_from_timestamps(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        
        timestamps_M15 = my_velas_M15.timestamps
        timestamps_M15 = timestamps_M15[:-10]
        
        special_days_dict = my_market_hours.estimate_special_trading_days_from_timestamps(timestamps_M15)
        special_date = dt.date(2019,8,20)
        
        assert my_market_hours.special_days_dict == special_days_dict
        assert list(special_days_dict.keys())[0] == special_date
        
    def test_index_by_days_dict(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        timestamps_M15 = my_velas_M15.timestamps
        
        ## Estimate things to get the parameters of the MarketHours
        my_market_hours.estimate_special_trading_days_from_timestamps(timestamps_M15)
        index_by_days_dict = MarketHours.get_index_by_days_dict(timestamps_M15)
        number_of_samples_per_trading_session = my_market_hours.get_number_of_samples_of_trading_session(my_velas_M15.timeframe)
        
        assert len(index_by_days_dict.keys()) == 22
        
        for date in index_by_days_dict.keys():
            daily_timestamps = index_by_days_dict[date]
            assert daily_timestamps.size == number_of_samples_per_trading_session


    def test_number_of_samples_by_weekday_dict(self):
        my_market_hours = get_loaded_market_hours()
        my_velas_M15 = get_loaded_Velas()
        timestamps_M15 = my_velas_M15.timestamps
        
        samples_by_weekday_dict = my_market_hours.get_number_of_samples_by_weekday_dict(timestamps_M15)
        
        days = [0,1,2,3,4]
        saved_dict = {0: 480, 1: 480, 2: 384, 3: 384, 4: 384}
        assert list(samples_by_weekday_dict.keys()) == days
        for day in days:
            samples_by_weekday_dict[day] = saved_dict[day]


        
