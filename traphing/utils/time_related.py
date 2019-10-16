import numpy as np
import pandas as pd
import datetime as dt
import time
import matplotlib.dates as mdates
from . import fnp

"""
####################### DATETIME HANDLING ######################
"""
def get_dates(dates_list):
    # Gets only the date from a timestapm. For a list
    only_day = []
    for date in dates_list:
        only_day.append(date.date())
    return np.array(only_day)


def get_times(dates_list):
    # Gets only the time from a timestapm. For a list
    only_time = []
    for date in dates_list:
        only_time.append(date.time())
    return np.array(only_time)
    

def str_to_datetime(dateStr):
    # This function converts a str with format YYYY-MM-DD HH:MM:SS to datetime
    dates_datetime = []
    for ds in dateStr:
        dsplited = ds.split(" ")
        date_s = dsplited[0].split("-") # Date
        
        if (len(dsplited) > 1):  # Somo files have hours, others does not
            hour_s = dsplited[1].split(":")  # Hour 
            datetim = dt.datetime(int(date_s[0]), int(date_s[1]), int(date_s[2]),int(hour_s[0]), int(hour_s[1]))
        else:
            datetim = dt.datetime(int(date_s[0]), int(date_s[1]), int(date_s[2]))
            
        dates_datetime.append(datetim)
    return dates_datetime

"""
##################### CONVERSIONS BETWEEN DATES ########################
"""

def convert_dates_str(X):
    # We want to convert the dates into an array of char so that we can plot 
    # this shit better, and continuous

    Xdates_str = []
    for date_i in X:
        name = date_i.strftime("%Y/%m/%d:%H:%M")
        Xdates_str.append(name)
    return Xdates_str


def to_mdates(timestamps):
    """function to return the timestamps in matplotlib format"""
    try: 
        if(len(timestamps.shape) > 1):
            timestamps = timestamps.flatten()
    except:
        print("fdbefgndfgsgnfdg")
        print(type(timestamps))
        pass
    return mdates.date2num(pd.to_datetime(timestamps).to_pydatetime())

def get_timeStamp(date):
    return time.mktime(date.timetuple())


def transform_time(time_formated):
    # This function accepts time in the format 2016-01-12 09:03:00
    # And converts it into the format [days] [HHMMSS]
    # Remove 
    
    data_normalized = []
    for time_i in time_formated:
        time_i = str(time_i)
#        print time_i
        time_i = time_i[0:19]
        time_i = time_i.replace("-", "")
        time_i = time_i.replace(" ", "")
        time_i = time_i.replace(":", "")
        time_i = time_i.replace("T", "")
#        print time_i
        data_normalized.append(int(time_i))
        
    return data_normalized 
    

def preprocess_dates(X):
    # Dealing with dates !
    ## Format of time in plot [736203.87313988095, 736204.3325892858]
    if (type(X).__name__ != "list"):
        if (type(X[0,0]).__name__ == "datetime64"):
            X = pd.to_datetime(X).T.tolist()  #  DatetimeIndex
            X = mdates.date2num(X)
#        else:  #  DatetimeIndex
#            X = X.T.tolist()[0]  
    return X
#        processed_dates =  ul.str_to_datetime (dataCSV.index.tolist())
#        pd.to_datetime('13000101', format='%Y%m%d', errors='ignore')

def convert2dt(dates):
    # Finally a function to convert an array of shit to datetime
    
    dates = fnp(dates).flatten()
    caca = []
    for date in dates:
        # date_new =  date.astype(dt.datetime) # This fucking converts it to a long !!
        date_new = pd.to_datetime(date)
#        print date, date_new
        caca.append(date_new)
    return caca
    
def matlab2datetime(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days = 366)
    return day + dayfrac

"""
##################### Other ########################
"""
def diff_dates(dates):
    # This function fucking computes the delta difference between the samples
    dates = convert2dt(dates)
    Ndates = len(dates)
    diffs = []
    for i in range(1,Ndates):
        diffs.append(dates[i] - dates[i-1])
    return diffs
    

def get_time_difference(open_time, close_time):
    return (close_time.hour - open_time.hour)*60 + (close_time.minute - open_time.minute) +  \
        (close_time.second - open_time.second)*60 # + (close_time.mircosecond - open_time.mircosecond)
        

