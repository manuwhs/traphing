
import datetime as dt
from . import Timeframes, diff_dates, get_time_difference
import pandas as pd


class SpecialMarketHours():
    """
    Class for special market hours.
    
    We know it is likely to be missing data if:
        - The open and close times are the regular ones but we lack samples
        - The is not contnuity in the samples
    
    We know it is likely that it is a reduced time if:
        - There is contnuity in the samples but the open and close time are unusual
        
    """
    def __init__(self, date, open_time = None, close_time = None,  n_samples = None):
        self.date = date 
        self.open_time = open_time
        self.close_time = close_time
        self.n_samples = n_samples
        
    def is_non_trading_day(self):
        if(self.n_samples is None):
            return True
        return False
    
class MarketHours():
    """
    This class is meant to handle all the information and processing related to
    the opening market hours of a given asset
    """
    
    seconds_in_a_day = 60*60*24
    
    @staticmethod
    def get_index_by_days_dict(timestamps: pd.DatetimeIndex, dates = None):
        """
        Create dictionary with dates as index an intraday timestamps as values
        """
        if(dates is None):
            dates = timestamps.map(pd.Timestamp.date)
        indexes_by_day_dict = timestamps.groupby(dates)
        return indexes_by_day_dict
    
    
    @staticmethod
    def add_timeframe_to_time(time, timeframe):
        """
        Fucking not implemented in the standard library for some reason
        """
        datetime = dt.datetime.now().replace(minute= time.minute, hour = time.hour, second = time.second, microsecond = 0) + dt.timedelta(minutes = timeframe.value)
        return datetime.time()
    
    def __init__(self, open_time = None, close_time = None, trading_days_list = None, special_days_dict = None):
        self.open_time = open_time
        self.close_time = close_time
        self.trading_days_list = trading_days_list
        self.special_days_dict = special_days_dict  # Dictionary with special dates  [start_time, close_time]
        
    def is_special(self, date):
        """
        It returns True if it knows it is a special day with abnormal trading hours
        """
        if date in list(self.special_days_dict.keys()):
            return True
        
        return False
    
    def should_be_usual_trading_day(self, date):
        return date.weekday() in self.trading_days_list
    
    
    def is_trading_day(self, date):
        """
        Returns True if the market is open for that day.
        It is open if it is an special day with trading hours or
        if it is in the normal trading hours.
        """
        
        if (self.is_special(date)):
            # It could be a special day where there is no trading
            if(self.special_days_dict[date].is_non_trading_day() == False):
                return True
        elif (self.should_be_usual_trading_day(date)):
            return True
        return False
        
    
    def is_market_open(self,timestamp):
        """
        Returns true if the market is open for the given timestamp
        """
        open_time, close_time = self.get_open_close_time(timestamp.date())
        
        after_open_bool = timestamp.hour*60 + timestamp.minute >= open_time.hour*60 + open_time.minute
        before_close_bool = timestamp.hour*60 + timestamp.minute <= close_time.hour*60 + close_time.minute
        
        return after_open_bool and before_close_bool
    
    """
    Getting core functions
    """
    def get_open_close_time(self, date = None):
        """
        Returns the open and close times of the market hours for a given day
        If no date is passed, then the normal times are assumed (if they were computed before)
        If 
        """
        if date is None:
            return self.open_time, self.close_time
        
        elif (self.is_special(date)):
            return self.special_days_dict[date].open_time, self.special_days_dict[date].close_time
        else:
            return self.open_time, self.close_time
    
    def get_length_session_in_seconds(self, date = None):
        """
        Compute the number of seconds the market is closed and open in a given day
        """
        open_time, close_time = self.get_open_close_time(date)

        seconds_open = (close_time.hour - open_time.hour)*3600 + \
                        (close_time.minute - open_time.minute)*60
        seconds_closed = MarketHours.seconds_in_a_day - seconds_open
        
        return seconds_open, seconds_closed
    
    
    def get_origin_reference_seconds(self, date = None):
        """
        We need an origin reference for the intraday date transformation
        """
        open_time, close_time = self.get_open_close_time(date)
        origin = dt.datetime(1970,1,5,open_time.hour, open_time.minute,open_time.second)
        return origin

    """
    Dealing with intraday and sessions
    """
    def does_session_start_in_previous_natural_day(open_time, close_time):
        """
        Depending on our TimeZone, it might happen that the trading session of a given day
        actually starts in the previous natural day. i.e 21:00 - 5:00 
        """
        time_difference = get_time_difference(open_time, close_time)
        if (time_difference < 0):
            return True
        return False
            
    
    def get_number_of_samples_of_trading_session(self, timeframe, date = None):
        """
        It computes the number of samples per normal trading session
        """
        open_time, close_time = self.get_open_close_time(date) 
        time_difference = get_time_difference(open_time, close_time)
        
        if (time_difference == 0):
            time_difference = 24*60 # 24h trading
            
        return int(time_difference/timeframe.value)         


    def get_number_of_samples_by_weekday_dict(self, timestamps):
        """
        Returns a dictionary with the weekdays as keys (int format) and the number
        of timestamps that belong to that weekday.
        It can be used for datetime and date timestamps.
        """
        weekdays = timestamps.map(pd.Timestamp.weekday)
        weekdays_dict = weekdays.groupby(weekdays)
        for key in weekdays_dict.keys():
            weekdays_dict[key] = weekdays_dict[key].size
        return weekdays_dict
        
    """
    Guessing from data functions
    """
    def estimate_timeframe(self, timestamps)-> Timeframes:
        """
        Estimates the timeframe of the time series.
        It does so by computing the minimum time distance between samples.
        """
        diffs = diff_dates(timestamps)
        minutes_timeframe = min(diffs).total_seconds() / 60
        timeframe = Timeframes(minutes_timeframe)
        return timeframe
    
    
    def estimate_open_close_time(self, timestamps, timeframe = None):
        if (timeframe is None):
            timeframe = self.estimate_timeframe(timestamps)
        indexes_by_day_dict = MarketHours.get_index_by_days_dict(timestamps)

        first_candlestick_time_in_natural_day_list = []
        last_candlestick_time_in_natural_day_list  = [] 
        
        for date in indexes_by_day_dict.keys():
            first_candlestick_time_in_natural_day_list.append(indexes_by_day_dict[date][0].time())
            last_candlestick_time_in_natural_day_list.append(indexes_by_day_dict[date][-1].time())  
            
        open_time = min(first_candlestick_time_in_natural_day_list)
        close_time = max(last_candlestick_time_in_natural_day_list) 
        close_time = MarketHours.add_timeframe_to_time(close_time, timeframe)
        
        self.open_time = open_time; self.close_time = close_time
        return open_time, close_time
  
 
    def estimate_normal_trading_days(self, timestamps, open_time = None, close_time = None,  timeframe = None):
        """
        Estimates the normal days in which the market is open for this commodity.
        If we know the timeframe and normal market hours, we can pass them as attributes.
        Otherwise we estimate them
        """
        if (timeframe is None):
            timeframe = self.estimate_timeframe(timestamps)
        if (open_time is None):
            open_time, close_time  = self.estimate_open_close_time(timestamps,timeframe)
        
        
        unique_days = timestamps.map(pd.Timestamp.date).unique()
        number_of_trading_days_dict = self.get_number_of_samples_by_weekday_dict(unique_days)
        
        trading_days_list = []
        for key in number_of_trading_days_dict.keys():
            if number_of_trading_days_dict[key] > 0:
                trading_days_list.append(key)
        
        self.trading_days_list = trading_days_list
        return trading_days_list
        
    
    def estimate_special_trading_days_from_timestamps(self, timestamps, open_time = None, 
                                                      close_time = None,  timeframe = None, trading_days_list = None):
        """
        Estimates the special trading days as those who do not follow the norm.
        TODO: Take DST into account.
        """
        if (timeframe is None):
            timeframe = self.estimate_timeframe(timestamps)
        if (open_time is None):
            open_time, close_time  = self.estimate_open_close_time(timestamps,timeframe)
        if (trading_days_list is None):
            trading_days_list = self.estimate_normal_trading_days(timestamps, open_time, close_time,  timeframe)
            
        number_of_samples_per_trading_session = self.get_number_of_samples_of_trading_session (timeframe)
        index_by_days_dict = MarketHours.get_index_by_days_dict(timestamps)
        special_days_dict = dict()        
        
        # Check for irregular days among the dates in the dataset
        for date in index_by_days_dict.keys():
            daily_timestamps = index_by_days_dict[date]
            
            special_day_flag = False
            special_open_time = open_time
            special_close_time = close_time
            
            if (daily_timestamps[0].time() != open_time):
                special_open_time = daily_timestamps[0].time()
                special_day_flag = True
                
            if (MarketHours.add_timeframe_to_time(daily_timestamps[-1].time(), timeframe) != close_time):
                special_close_time = MarketHours.add_timeframe_to_time(daily_timestamps[-1].time(), timeframe)
                special_day_flag = True
            
            if (daily_timestamps.size != number_of_samples_per_trading_session):
                special_day_flag = True
            
            if (special_day_flag):
                special_market_hours = SpecialMarketHours(date, special_open_time, special_close_time, daily_timestamps.size)
                special_days_dict[date] = special_market_hours
                
        # Check for missing dates that should be there
        unique_ordered_dates_list = list(index_by_days_dict.keys())
        first_date = unique_ordered_dates_list[0]
        last_date = unique_ordered_dates_list[-1]
        
        date = first_date
        while (date < last_date):
            date += dt.timedelta(days = 1)
            if(self.should_be_usual_trading_day(date) and (date not in unique_ordered_dates_list)):
                special_market_hours = SpecialMarketHours(0, None, None)
                special_days_dict[date] = special_market_hours
    
        self.special_days_dict = special_days_dict
        return special_days_dict
    
    """
    ################### Intraday Transformation ######################
    """
    def to_seconds_since_origin_without_intraday_gaps(self, date = None, fake_daily_minutes_gap = 60):
        origin = self.get_origin_reference_seconds(date)
        n_seconds_open, n_seconds_closed = self.get_length_session_in_seconds(date)
        
        # Compute number of days past since origin
        n_seconds_since_origin = (date - origin).total_seconds()
        n_days_since_origin = int(n_seconds_since_origin/MarketHours.seconds_in_a_day)
        n_weeks_since_origin = int(n_seconds_since_origin/(MarketHours.seconds_in_a_day*7))

        # Move to the left according to the number of days that have passed,
        # erasing the closed time of the market and adding the gap
        seconds_since_origin_without_intraday_gaps = n_seconds_since_origin - n_seconds_closed * n_days_since_origin \
                 - (2*n_seconds_open * n_weeks_since_origin) \
                 + 60*fake_daily_minutes_gap* n_days_since_origin
    
        return seconds_since_origin_without_intraday_gaps
    
    
    def from_seconds_since_origin_without_intraday_gaps_to_timestamps(self, transformed_seconds_since_origin = None, fake_daily_minutes_gap = 60):
        
        # TODO: Problem is, we do not know the date before we transform it... so it is hard to detransform
        # if we allow different dates to have different trading times
        
        origin = self.get_origin_reference_seconds()
        n_seconds_open, n_seconds_closed = self.get_length_session_in_seconds()
        
        n_weeks_past = int(transformed_seconds_since_origin/((5*n_seconds_open + 7*60*fake_daily_minutes_gap)))
        n_seconds_weeks_added = transformed_seconds_since_origin + n_weeks_past*2*n_seconds_open 
        n_days_past = int(n_seconds_weeks_added/(n_seconds_open + 60*fake_daily_minutes_gap))
        
        n_seconds = n_seconds_weeks_added + n_days_past*n_seconds_closed - 60*fake_daily_minutes_gap*n_days_past
        timedelta = dt.timedelta(seconds=n_seconds)
        timestamp = origin + timedelta
        
        return timestamp