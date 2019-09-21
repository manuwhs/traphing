
import numpy as np
import pandas as pd
import datetime as dt
import time

#########################################################
#################### TIME FUNC ##########################
#########################################################

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
    
import matplotlib.dates as mdates
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
def convert_dates_str(X):
    # We want to convert the dates into an array of char so that we can plot 
    # this shit better, and continuous

    Xdates_str = []
    for date_i in X:
        name = date_i.strftime("%Y/%m/%d:%H:%M")
        Xdates_str.append(name)
    return Xdates_str

def diff_dates(dates):
    # This function fucking computes the delta difference between the samples
    dates = convert2dt(dates)
    Ndates = len(dates)
    diffs = []
    for i in range(1,Ndates):
        diffs.append(dates[i] - dates[i-1])
    return diffs
    
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
    
def transformDatesOpenHours(dates, opentime, closetime, minuts_sep = 60):
    """
    This funciton transform the dates to a scale where the intraday 
    would be together from one day to the other
    The minuts_sep  is the separation of minuts between the days.
    """
    ndates = dates.size
    transformed_seconds = np.zeros((ndates,1))
    
    # We set a distant random day as the origin. The only important thing is 
    # that the starting time should be the same as the market time. If we want to erase mondays,
    # it should also be monday ? 

    origin = dt.datetime(1970,1,5,opentime.hour, opentime.minute,opentime.second)
    dt.datetime(1970,1,6).weekday()
    # Make sure the dates are in format of pandas datetime
    dates = convert2dt(dates)

    ## Compute the number of seconds the market is closed and open in a day
    nseconds_day = 60*60*24
    nseconds_open = (closetime.hour - opentime.hour)*3600 + \
                    (closetime.minute - opentime.minute)*60
    nseconds_closed = nseconds_day - nseconds_open
    
#    print nseconds_day, nseconds_open, nseconds_closed
#    print "---"
    for i in range(ndates):
        nseconds = (dates[i] - origin).total_seconds()
        # Compute number of days past since origin
        ndays_past = int(nseconds/nseconds_day)
        nweeks_past = int(nseconds/(nseconds_day*7))
#        print nweeks_past
        # Move to the left according to the number of days that have passed,
        # erasing the closed time of the market and adding the gap
        transformed_seconds[i,0] = nseconds - nseconds_closed * ndays_past
        transformed_seconds[i,0] -= 2*nseconds_open * nweeks_past
        transformed_seconds[i,0] += 60*minuts_sep* ndays_past
        
      
#        transformed_seconds[i,0] = ndays_past * (nseconds_open + 60*minuts_sep)
    return transformed_seconds

def detransformDatesOpenHours(transformed_dates,opentime, closetime, minuts_sep = None):
    """
    This function detransforms the date so we can know what time they actually are
     and also being able to automatically format the xlables in python
    """
    if (type(minuts_sep) == type(None)):
        minuts_sep = 60
    origin = dt.datetime(1970,1,5,opentime.hour, opentime.minute,opentime.second)

    transformed_dates = fnp(transformed_dates).flatten()
    ndates = transformed_dates.size
    dates = []
    # Now, virtually every day only lasts nseconds_open + nseconds_open
#    print type(dates[0])
    nseconds_day = 60*60*24
    nseconds_open = (closetime.hour - opentime.hour)*3600 + \
                    (closetime.minute - opentime.minute)*60
    nseconds_closed = nseconds_day - nseconds_open
    
#    print nseconds_day, nseconds_open, nseconds_closed
    for i in range(ndates):
        nweeks_past = int(transformed_dates[i]/((5*nseconds_open + 7*60*minuts_sep)))
        nseconds_weeks_added = transformed_dates[i] + nweeks_past*2*nseconds_open 
        ndays_past = int(nseconds_weeks_added/(nseconds_open + 60*minuts_sep))
        
#        transformed_seconds[i,0] = nseconds - ((nseconds_closed - 60*minuts_sep)* ndays_past) 
        nseconds = nseconds_weeks_added + ndays_past*nseconds_closed - 60*minuts_sep*ndays_past
        nseconds = float(nseconds)
        deltadate = dt.timedelta(seconds=nseconds)
        date = origin + deltadate
        dates.append(date)
    return dates

class deformatter_data:
    def __init__(self, opentime, closetime, minuts_sep):
        self.opentime = opentime    # Symbol of the Security (GLD, AAPL, IDX...)
        self.closetime = closetime
        self.minuts_sep = minuts_sep

def detransformer_Formatter(x,pos):
    # This function will use 
#    detransformer_Formatter.format_data = None
    dates = detransformDatesOpenHours(x, detransformer_Formatter.format_data.opentime,
                                      detransformer_Formatter.format_data.closetime,
                                      detransformer_Formatter.format_data.minuts_sep)
    date = dates[0] # We actually only receive one date
    return date.strftime('%Y-%m-%d %H:%M')
    
def matlab2datetime(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days = 366)
    return day + dayfrac