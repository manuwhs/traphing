# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import datetime as dt

from ... import utils

################# CSV FUNCTIONS #########################

def get_csv_file_path(self):
    """ Generates the filename convention of the csv"""
    file_path = utils.get_csv_file_path(self.symbol_name, self.timeframe)
    return file_path

def save_to_csv(self, storage_folder = "./storage/", force = False):
    """ Save the underlaying dataframe to csv with a security measure
    in case it was trimmed"""
    if (self.is_trimmed() and force == False):
        print ("You cannot save the file since you trimmed it, Use force = True")
    else:
        file_path = storage_folder + self.get_csv_file_path()
        utils.create_folder_if_needed(utils.get_file_dir(file_path))
        self._df.to_csv(file_path, sep=',')

def load_data_from_csv(self, storage_folder = "./storage/"):    
    df = utils.load_data_from_csv(self.symbol_name,self.timeframe, storage_folder)
    self.df = df
    
def add_data_from_csv(self, storage_folder = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    df = utils.load_data_from_csv(self.symbol_name,self.timeframe, storage_folder)
    self.add_df(df)

def update_csv (self, storage_folder, updates_folder):
    # Function that loads from 2 different folders, joins the data and saves it back
    self.load_data_from_csv(storage_folder)
    self.add_data_from_csv(updates_folder)
    self.save_to_csv(storage_folder)


######################################################################
############## BBDD data processing ###################################
#######################################################################

def fill_data(self):
    data_TD = self.get_TD()
    ninit = data_TD.shape[0]
    data_TD = intl.fill_by_filling_everything(data_TD, self.start_time, self.end_time)
    nend = data_TD.shape[0]
    self.set_TD(data_TD)
    if (nend > ninit):
        msg = "Missing : %i / %i" % (nend - ninit, nend)
        print (msg)
        
def get_intra_by_days(self):
    result = intl.get_intra_by_days(self.dates, self.get_timeSeries())
    return result
    
def check_data(self):  # TODO
    # Check that there are no blanck data or wrong
    print ("checking")
    
def data_filler(self): # In case we lack some data values
    # We can just fill them with interpolation
    # We do this at csv level 

    self.dailyData 
    start_date = self.dailyData.index[0].strftime("%Y-%m-%d")   #strptime("%Y-%m-%d")
    end_date = dt.datetime(self.dailyData.index[-1].strftime("%Y-%m-%d"))
    
    print (start_date)
    # We have to get all working days between these 2 dates and check if
    # they exist, if they dont, we fill them
    # Create days of bussines
    
    busday_list = []
    
    next_busday = np.busday_offset(start_date, 1, roll='forward')
    busday_list.append(next_busday)
    
    while (next_busday < end_date): # While we havent finished
#        print next_busday, end_date
        next_busday = np.busday_offset(next_busday, 1, roll='forward')
        busday_list.append(next_busday)

    Ndays_list = len(busday_list)   # Number of days that there should be
    Ndays_DDBB = len(self.dailyData.index.tolist())
    
    print (Ndays_list, Ndays_DDBB)  ## TODO
    
    
#    for i in range (Ndays_list):
#        print "e"
        
    print (start_date, end_date)


def fill_in_missing_dates(df, date_col_name = 'date',date_order = 'asc', fill_value = 0, days_back = 30):

    df.set_index(date_col_name,drop=True,inplace=True)
    df.index = pd.DatetimeIndex(df.index)
    d = datetime.now().date()
    d2 = d - timedelta(days = days_back)
    idx = pd.date_range(d2, d, freq = "D")
    df = df.reindex(idx,fill_value=fill_value)
    df[date_col_name] = pd.DatetimeIndex(df.index)

    return df


def data_filler_main_TD():
    time_diff = intl.find_min_timediff(self.get_timeData())
#    print time_diff
#    print type(time_diff)
    
#    idx = intl.get_pdintra_by_days(timeData.TD)
    
    ## Fill the interspaces, create another timeSeries and plot it
    filled_all = intl.fill_everything(self.get_timeData())
    
    timeData2 = copy.deepcopy(timeData)
    timeData2.set_timeData(filled_all)
    timeData2.get_timeSeries(["Close"])
    timeData2.plot_timeSeries()
    print (timeData2.get_timeSeries().shape)
    
    ## Fill missing values by first filling everythin
    filled = intl.fill_by_filling_everything(self.get_timeData())
    timeData2 = copy.deepcopy(timeData)
    timeData2.set_timeData(filled)
    timeData2.get_timeSeries(["Close"])
    timeData2.plot_timeSeries(nf = 0)
    print (timeData2.get_timeSeries().shape)
    
    ### Get the day table
    pd_dayly = intl.get_dayCompleteTable(timeData.get_timeData())
    time_index = intl.find_trade_time_index(timeData.get_timeData())
    index_shit = intl.find_interval_date_index(timeData.get_timeData(), dt.date(2016,3,1),  dt.date(2016,5,1))



    self.add_IntraData(data_intra_google)