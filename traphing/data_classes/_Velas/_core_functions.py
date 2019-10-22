import numpy as np
import copy
import pandas as pd
from ...import indicators  as ind

############  Time realted ##########################
def _get_time_mask(start_time, end_time, dates):
    """
    Generates the time mask to subselect a time interval
    """
    time_mask = (dates.date >= start_time.date()) & \
                    (dates.date <= end_time.date())
    # Transform boolean mask to index mask
    time_mask = np.argwhere(time_mask).T[0]
    return time_mask


def set_time_interval(self, start_time = None, end_time = None, trim = False):
    """
    Set the time interval of the velas.
    If trim == True then, the velas outside of the interval will be removed.
    A binary time mask will be created in case it is not trimmed to select the
    correct dates.
    """
    all_timestamps = self._df.index
    
    if all_timestamps.size == 0:
        return False        
    if start_time is None:   
        start_time = all_timestamps[0]
    if end_time is None:
        end_time = all_timestamps[-1]
    
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    
    self._time_mask = _get_time_mask(start_time, end_time, all_timestamps )    
    self.start_time, self.end_time = start_time, end_time    
    if (trim):
        self._trim_df(self._time_mask)
    return True

################# Specific fetching functions #####################
def get_candlestick(self, datetime):
    """ It returns the closest candlestick with timestamp before 
    """
    try:
        row = self.df.loc[[datetime], : ]
    except:
        row = self.get_closest_past_candlestick(datetime)
    return row


def get_closest_past_candlestick(self, datetime):
    """
    Gets the last candlesick that comes before the provided datetime.
    """
    diff = self.timestamps - datetime
    indexmax = np.argmax(diff[(diff < pd.to_timedelta(0))])
    row = self.df.iloc[[indexmax]]
    return row


################# Dataframe functions ##########################
def is_trimmed(self):
    return self._trimmed


def add_df(self, df:pd.DataFrame):
    """This function adds new data to the existing data 
     It places it into the positions refered by the "Index" date.
     If there are days with the same index, they get overwritten.
        self.dailyData = pd.concat([self.dailyData, new_dailyData], verify_integrity = True)
        self.dailyData = pd.merge(self.dailyData, new_dailyData)
    """
    df = df.combine_first(self._df) 
    self.df = df  


def _trim_df(self, time_mask):
    # This function receives the list of indexes of the new TD and erases the rest
    self._trimmed = True   
    df = self._df.iloc[time_mask]
    self.df = df
    
    
def series(self, name):
    """
    The basic series need to be able to be computed only using a single candlestick
    options = ["Open","Close","High","Low","Volume","Average", "RangeHL","RangeCO"]
    """
    if (name == "Average"):
        timeSeries = np.mean(self.df[["Low","High","Close","Open"]], axis = 1)
    
    elif(name == "RangeHL"):  # Difference Between High and Low
        Range = self.df["High"] - self.df["Low"]
        timeSeries = Range
        
    elif(name == "RangeCO"):  # Difference between Close and Open
        Range = self.df["Close"] - self.df["Open"]
        timeSeries = Range
    else:
        timeSeries = self.df[name]
    
    return timeSeries


def indicator(self, name = "SMA", *args, **kwargs):
    """
    Incators can use any candlestick in the data.
    """
    try:
        #method_func = getattr(self, method_name)
        indicator_func = getattr(ind, name)
    except AttributeError:
#        raise Warning("method_name: '%s' does not exist in the Velas object"%name)
        raise Warning("indicator_func: '%s' does not exist in the indicator library"%name)
#    kwargs["df"] = self.df ## TODO: Maybe this way is better in the future
    return indicator_func(df = self.df, *args, **kwargs)
