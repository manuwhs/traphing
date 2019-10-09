# -*- coding: utf-8 -*-
#import matplotlib

###### IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
## Si devolvemos algun self.XXXX, devolver un copy.deepcopy()
import numpy as np
import copy
import time
import pandas as pd
import datetime as dt
"""
Library with all the obtaining indicator functions of the market.

"""
def _get_time_mask(start_time, end_time, dates):
    """
    Generates the time mask
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
    dates = self._df.index
    
    if(dates.size == 0):
        return False    #We cannot do anything
    
    if (start_time is None):   # Case of nothing given
        start_time = dates[0]
        
    if (end_time is None):
        end_time = dates[-1]
    
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    
    self._time_mask = _get_time_mask(start_time, end_time, dates )
    
    self.start_time = start_time
    self.end_time = end_time 
    
    if (trim):
        self._trim_df(self._time_mask)
    
    return True

################# TableData FUNCTIONS ##########################

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
    

def preprocess_RAW_TD(self, Raw_TD):

    # This function preprocess the RAW table of data into a TD.
    # Which is basically processing the "Date" part. It is inline
    # TODO: Maybe some processing on the "Date part"
    
    processed_dates = pd.to_datetime(Raw_TD.index)
    Raw_TD.index = processed_dates
    return Raw_TD

def series(self, name):
    """
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
        
#    elif(name == "Gaps"):  # Difference between Close and Open
#        magicDelta = self.get_magicDelta()
#        timeSeries = magicDelta
        
    else:
        timeSeries = self.df[name]
    
    return timeSeries
    
    
if(0):    
    ##########################################################
    ################ GETTING FUNCTIONS #######################
    ##########################################################
    

    
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
        
        
    
    ######################   GUESSING PROPERTIES OF THE DATA   ######################
    

    
    ##################################################################
    ######################   DIFERENCES DATA    ######################
    ##################################################################
    """  Here we define other time series obtained from linear operations
    over the basic ones"""
    
    def get_magicDelta(self):
        closePrev = self.df["Close"].values
        openCurr = self.df["Open"].values
    
        magicDelta = np.array(openCurr[1:] - closePrev[:-1])
        magicDelta = np.concatenate(([0],magicDelta), axis = 0)
        
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
        
