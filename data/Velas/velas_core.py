# -*- coding: utf-8 -*-
#import matplotlib

###### IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
## Si devolvemos algun self.XXXX, devolver un copy.deepcopy()
import numpy as np
import copy
import time
import pandas as pd
import graph_lib as gr
import Intraday_lib as itd
import utilities_lib as ul
import indicators_lib as indl
import get_data_lib as gdl 
import basicMathlib as bMl

import datetime as dt
from datetime import datetime
"""
Library with all the obtaining indicator functions of the market.

"""

# Start Date is the date from which we return the data.
# The data returned should be returned after this date.

# TimeSeries is the main data we have to care about. 
# All the operations will be done over this one

    
class MarketHours():
    """
    This class is meant to handle all the information and processing related to
    the opening market hours of a given asset
    """
    def __init__(self):
        self.open_time = None
        self.close_time = None
        
    def estimate_openMarketTime(self):
        # If we do not know the period in which the market should be open, this function
        # will try to guess it from the data. There is some weird assets like the Forex
        # that are only open one hour on Sundays. Also, the timeZone can create problems.
        
        openTimes = []
        closeTimes = [] 
        
        dates = self.get_dates()
        days, indexDaysDict = self.get_indexDictByDay()
    #    print days
        for day in days:
            openTimeindex = indexDaysDict[day][0]
    #        print openTimeindex
            openTimes.append(dates[openTimeindex].time())
            closeTimes.append(dates[indexDaysDict[day][-1]].time())
            
        openTime = min(openTimes)
        closeTime = max(closeTimes)
        
        return [openTime, closeTime]
    
    
def _get_time_mask(start_time, end_time, dates):
    """
    Generates the time mask
    """

    time_mask = (dates.date >= start_time.date()) & \
                    (dates.date <= end_time.date())
    # Transform boolean mask to index mask
    time_mask = np.argwhere(time_mask).T[0]
    
    return time_mask

def set_time_interval(self, start_time = None, end_time = None, trim = True):
    """
    Set the time interval of the velas.
    If trim == True then, the velas outside of the interval will be removed.
    A binary time mask will be created in case it is not trimmed to select the
    correct dates.
    """
    dates = self.dates
    
    if (start_time is None):   # Case of nothing given
        start_time = dates[0]
    if (end_time is None):
        end_time = dates[-1]
        
    self._time_mask = _get_time_mask(start_time, end_time, dates )
    
    self.start_time = start_time
    self.end_time = end_time 
    
    if (trim):
        self.trim_OCHLV(self.time_mask)

        
        
##########################################################
################ GETTING FUNCTIONS #######################
##########################################################

def get_timeSeriesbyName(self, name, indexes = []):
    ## This function returns the time series selected by the name
    # The final timeSeries will be [Nsamples][Nsec]
    # The name could imply a transformation of the original data stored
    # indexes is a binary array that indicates the  samples we want to obtain.
    # If not specified, we use the internal mask.

    # The index is referenced 
    if (len(indexes) == 0):
        # If we do not specify indexes
        indexes = self.time_mask
#    else:
#        indexes = np.array(indexes,dtype = bool)
#    print indexes
    if (name == "Average"):
        timeSeries = np.mean(self.TD[["Low","High","Close","Open"]].values[indexes], axis = 1)
    
    elif(name == "RangeHL"):  # Difference Between High and Low
        Range = np.array(self.TD["High"][indexes] - self.TD["Low"][indexes])
        timeSeries = Range
        
    elif(name == "RangeCO"):  # Difference between Close and Open
        Range = self.TD["Close"][indexes] - self.TD["Open"][indexes]
        timeSeries = Range
        
    elif(name == "magicDelta" or name == "Gap" ):  # Difference between Close and Open
        magicDelta = self.get_magicDelta(indexes)
        timeSeries = magicDelta
        
    else:
        timeSeries = self.TD[name][indexes]
        
    if (len(indexes) == 0):
        # If we do not specify indexes
        self.timeSeries = timeSeries

#    timeSeries = timeSeries[self.time_mask]    # Price List we are operating with timeSeries[Nvalues][Ndates]
#    print timeSeries
    return timeSeries


def cmp_indexes(self, indexes):
    # Outputs 1 if the indexes are the same and 0 otherwise
    # It only checks the first and last positions.
    if (len(indexes) == 0): # If empty
        return 1
    if (indexes[0] == self.time_mask[0]) and (indexes[-1] == self.time_mask[-1]):
        return 1
    else:
        return 0
    return 1
    
def get_indexDictByDay(self, TD = None):
    """ 
    This function gets the index of the dates, divided by days.
    It returns a dictinary where every key is a day and the value is the list of index
    This function works with bult in pandas dataframe functions.
    
    It returns the list of days ordered and the dictionary with the indexes associated
    to each of the days
    """
#    dates = self.get_dates()

    if (type(TD) == type(None)):
        TD = self.TD
    dates = TD.index.date
    caca = TD.groupby(dates)
    groups_of_index_dict = caca.groups # This is a dictionary with the dates as keys and the indexes of the TD as values
    
    days_dict = caca.indices # This is a dictionary with the dates as keys and the indexes of the TD as valu
    days_keys = list(days_dict.keys())# list of datetime.date objects
    days_keys.sort() 
    
    if(0):
        # Not needed if the sequence was already ordered
        for k in days_keys:
           days_dict[k].sort()
#        set_indexes = days_dict[keys[0]].sort()
    
    return days_keys, days_dict
    
def get_timeSeriesReturn(self, seriesNames = [], indexes = [], transform = "no"):
    # Gets the Return of the Time Series, if it has not been created yet, then it creates it
    # if (self.timeSeries == []):  # Check existence of timeSeries

    # We will try as well to get the return of the first datapoint
    # if we actually have it in the database. For this, we check our mask.
    # If the first "1" found is not at 0, we can do this
    self.set_inner_timeSeries(seriesNames, indexes)
    timeSeries = self.get_timeSeries(seriesNames, indexes, transform = "tus muertos")

    # Position of the first sample we are using
#    pos1 = self.time_mask[0] 
    
    # TODO. Make it work for series Names not in the dataset.
#    if (pos1 > 0 and self.period >= 1440): # If we actually have more signal.
    if(0):
        # We could compute the real previous return by concatenating the previous
        # sample, computing the return and then removinf the first 0
        
        # For now it only works if the time series is one of the originals, not the
        # transformations, because then we have to get the transformation and we dont want to
#        ps = self.TD[self.seriesNames].iloc[pos1-1]
#        ps = np.array(ps).T
#        ps = ps.reshape(ps.size/len(self.seriesNames), len(self.seriesNames))
        
        ## We obtain the returns of the signal adding the previous.
        
        timeSeriesPlus = self.get_timeSeries(indexes = np.insert(indexes, 0, pos1-1))
#        print timeSeriesPlus.shape
        self.timeSeriesReturn = bMl.get_return(timeSeriesPlus)
        self.timeSeriesReturn = self.timeSeriesReturn[1:,:]
    else:
        self.timeSeriesReturn = bMl.get_return(timeSeries)
    
    if (transform == "log"):
    ## We perform log of this shit + 1 to get the log returns
        self.timeSeriesReturn = np.log(self.timeSeriesReturn + 1)
    
    return copy.deepcopy(self.timeSeriesReturn)

def get_timeSeriesCumReturn(self,seriesNames = [], indexes = [],):
    # Gets the Return of the Time Series, if it has not been created yet, then it creates it
    #if (self.timeSeries == []):  # Check existence of timeSeries
    timeSeriesReturn = self.get_timeSeriesReturn(seriesNames, indexes)
    timeSeriesCumReturn = np.cumsum(timeSeriesReturn, axis = 0)
    
    self.timeSeriesCumReturn = timeSeriesCumReturn
    return copy.deepcopy(timeSeriesCumReturn)

######################   GUESSING PROPERTIES OF THE DATA   ######################

def estimate_timeframe(self):
    # If we do not know the period of the signal a priori, we will try to guess it
    # This function is automatically called if the period is None and need to be used.
    dates = self.get_dates()
#    dates = ul.convert2dt(dates)
#    diffs = dates[1:] - dates[:-1]
#             # bMA.diff(dates)
    diffs = ul.diff_dates(dates)
#    print diffs
    min_pediod_min = min(diffs).total_seconds() / 60
    return min_pediod_min


##################################################################
######################   DIFERENCES DATA    ######################
##################################################################
"""  Here we define other time series obtained from linear operations
over the basic ones"""

def get_magicDelta(self, indexes = []):
    # Difference between the open of one day and the close of the preceiding day
    if (len(indexes) == 0):
        indexes = self.time_mask
        
    closePrev = self.TD["Close"][indexes].values
    openCurr = self.TD["Open"][indexes].values

    magicDelta = np.array(openCurr[1:] - closePrev[:-1])
    magicDelta = np.concatenate(([0],magicDelta), axis = 0)
#    print magicDelta
#    print len(openCurr[1:])
#    print (magicDelta.shape)
    
    return magicDelta

def get_diffPrevCloseCurrMax(self):
    
    # Difference between the open of one day and the close of the preceiding day
    PrevClose = self.TD["Close"].values
    CurrMax = self.TD["High"].values

    diffPrevCloseCurrMax = np.array(PrevClose[1:] - CurrMax[:-1]).reshape((len(PrevClose)-1,1))
    zero_vec = np.zeros((1,1))  # Add zero vector
    diffPrevCloseCurrMax = np.concatenate((zero_vec,diffPrevCloseCurrMax), axis = 0)
    
    return copy.deepcopy(diffPrevCloseCurrMax[self.time_mask,:])

def get_diffPrevCloseCurrMin(self):
    
    # Difference between the open of one day and the close of the preceiding day
    PrevClose = self.TD["Close"].values
    CurrMin = self.TD["Low"].values

#    print len(PrevClose)
    diffPrevCloseCurrMin = np.array(PrevClose[1:] - CurrMin[:-1]).reshape((len(PrevClose)-1,1))
    zero_vec = np.zeros((1,1))  # Add zero vector
#    print diffPrevCloseCurrMin.shape
    diffPrevCloseCurrMin = np.concatenate((zero_vec,diffPrevCloseCurrMin), axis = 0)
    
    return copy.deepcopy(diffPrevCloseCurrMin[self.time_mask,:])
    
