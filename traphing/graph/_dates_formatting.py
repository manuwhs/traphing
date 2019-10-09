import matplotlib.pyplot as plt
from .. import utils as ul
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

import numpy as np
import datetime as dt
import pandas as pd

def transform_to_seconds_without_intraday_gaps(timestamps: pd.DatetimeIndex, market_hours: ul.MarketHours,  fake_daily_minutes_gap = 60):
    """
    This funciton transform the dates to a scale where the intraday 
    would be together from one day to the other
    The minuts_sep  is the separation of minuts between the days.
    
    # We set a distant random day as the origin. The only important thing is 
    # that the starting time should be the same as the market time. If we want to erase mondays,
    # it should also be monday ? 
    """

    n_timestamps = timestamps.size
    transformed_seconds = np.zeros((n_timestamps,1))
    timestamps = ul.convert2dt(timestamps)
    for i in range(n_timestamps):
        transformed_seconds[i,0] = market_hours.to_seconds_since_origin_without_intraday_gaps(timestamps[i], fake_daily_minutes_gap)
    
    return transformed_seconds

def detransform_from_seconds_without_intraday_gaps(transformed_seconds, market_hours: ul.MarketHours,  fake_daily_minutes_gap = 60):
    """
    This function detransforms the date so we can know what time they actually are
     and also being able to automatically format the xlables in python
    """
    timestamps = []
    
    for i in range(transformed_seconds.size):
        timestamps.append(transformed_seconds[i,0])
    return timestamps


class IntradayTickFormatter:
    def __init__(self,market_hours, fake_daily_minutes_gap = 60):
        self.market_hours = market_hours    # Symbol of the Security (GLD, AAPL, IDX...)
        self.fake_daily_minutes_gap = fake_daily_minutes_gap


def detransformer_Formatter(x,pos):
    # This function will use 
#    detransformer_Formatter.format_data = None
    dates = detransform_from_seconds_without_intraday_gaps(x, detransformer_Formatter.format_data.opentime,
                                      detransformer_Formatter.format_data.closetime,
                                      detransformer_Formatter.format_data.minuts_sep)
    date = dates[0] # We actually only receive one date
    return date.strftime('%Y-%m-%d %H:%M')


