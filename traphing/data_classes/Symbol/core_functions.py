# -*- coding: utf-8 -*-
#import matplotlib

import numpy as np

from ...data_classes import Velas
from ...utils import Timeframes

"""
Library with all the obtaining indicator functions of the market.

"""

# Start Date is the date from which we return the data.
# The data returned should be returned after this date.

# TimeSeries is the main data we have to care about. 
# All the operations will be done over this one


########### Initialization functions ##############
def _create_velas(self, timeframes_list):
    for timeframe in timeframes_list:
        self.add_velas(timeframe)
        
######################################################################
######################## Interface functions to velas ###############
######################################################################

def add_velas(self, timeframe: Timeframes, velas: Velas = None):
    # This function adds the timeData object to the Symbol.
    # The timeDataObj is already an intialized timeDataObj.
    # We actually do not need to specify the period as we could
    # get it from the timeDataObj but this is more visual
    if (velas is None):
        velas = Velas(self.symbol_name, timeframe);
    self._velas_dict[timeframe] = velas

def del_velas(self, timeframe: Timeframes):
    # This function deletes the timeData object to the Symbol.
    del self._velas_dict[timeframe] 
    
#    CTD.CTimeData(self.symbol, period,timeData);

####################################################################
######## Functions to apply to all timeDatas #################
######################################################################

def set_time_interval(self,start_time = None, end_time = None, trim = True):
    for timeframe in self.timeframes_list:
        self[timeframe].set_time_interval(start_time, end_time, trim = trim)

######################################################################
######################## Basic Interface to timeDatas ###############
######################################################################

def get_currentPrice (self):
    # This function gets the current price from the lowest source
    minimumTimeScale = np.min(self.get_periods())
    currentPrice = self.timeDatas[minimumTimeScale].TD["Close"][-1]
    return currentPrice

def get_priceDatetime (self, datetime_ask, period):
    # This function gets the price for the given date in the given timeScale
    minimumTimeScale = np.min(self.get_periods())
    dates = self.timeDatas[period].TD.index
#    print datetime_ask
    good_dates = dates[dates == datetime_ask]
    good_prices = self.timeDatas[period].TD[dates == datetime_ask]["Close"]
    
#    print good_prices
    return good_prices[-1]
    
#########################################################
################# DATAFILLING ###########################
#########################################################

## This is the data filling function !!
## Define cases of datafilling !!