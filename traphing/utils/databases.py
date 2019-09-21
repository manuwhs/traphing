#########################################################3
############### DDBB LIBRARY  ##############################
##########################################################
## Library with function to manage the databases

import pandas as pd
import numpy as np

import datetime as dt

from .. import utils

def read_NASDAQ_companies(whole_path = "./storage/Google/companylist.csv"):
    # Function that reads the companies from the info file from NASDAQ
    # URL: http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download
    dataCSV = pd.read_csv(whole_path,
            sep = ',')
    
    return dataCSV
    
def save_to_csv(symbol,dataCSV, file_dir = "./storage/"):
    utils.create_folder_if_needed(file_dir)
    whole_path =  file_dir + symbol + ".csv"
    dataCSV.to_csv(whole_path, sep=',')

def load_csv_timeData(symbol, file_dir = "./storage/"):

    whole_path = file_dir + symbol + ".csv"
    try:
        dataCSV = pd.read_csv(whole_path,
                          sep = ',', index_col = 0, dtype = {"Date":dt.datetime})
    
        dataCSV.index = utils.str_to_datetime (dataCSV.index.tolist())
        
    except IOError:
        error_msg = "File does not exist: " + whole_path 
        print (error_msg)
    except:
        print ("Unexpected error in file: " + whole_path)
    # We transform the index to the real ones
    return dataCSV

def load_dataset(file_dir = "./dataprices.csv"):
    # Reads the dataprices
    data = pd.read_csv(file_dir, sep = ',') # header = None, names = None  dtype = {'phone':int}
    Nsamples, Ndim = data.shape   # Get the number of bits and attr

    return data

def download_and_add(list_symbols, sdate = "01-01-1996",
                     edate = "01-01-2016", fir_dir =  "./storage"):
    
    for symbol in list_symbols:
        data_Symbol = gdl.get_data_yahoo (symbol = symbol,  precision = "1mo", 
                  start_date = sdate, end_date = edate)
                  
        save_to_csv(symbol = symbol, 
                    dataCSV = data_Symbol)
"""
############## CSV related functions ################################
"""

def get_csv_file_path(symbol_name, timeframe):
    """ Generates the filename convention of the csv"""
    file_path =  utils.period_dic[timeframe] + "/" + \
            symbol_name + "_" + utils.period_dic[timeframe] + ".csv"
    return file_path

def load_data_from_csv(symbol_name, timeframe, storage_folder = "./storage/"):
    # This function loads the data from the file  file_dir + file_name if file_name is provided
    # Otherwise it uses the naming convention to find it from the root folder:
    # The file must have the path:  ./TimeScale/symbolName_TimeScale.csv
    
    # If we did not specify the symbolID or period and we set them in the 
    # initialization it will get them from there
    # specific and adds its values to the main structure
    
#    print("Setting csv: ", file_dir, ",symbol: ", symbolID,", period: ", period, ".File_name:",file_name)
    
    whole_path = storage_folder + get_csv_file_path(symbol_name, timeframe)
    
    try:
        dataCSV = pd.read_csv(whole_path, sep = ',', index_col = 0, header = 0)
        processed_dates = pd.to_datetime(dataCSV.index)
        dataCSV.index = processed_dates
    except IOError:
        error_msg = "File does not exist: " + whole_path 
        print (error_msg)
        dataCSV = utils.get_empty_df()
    
    print ("Size " + whole_path +": ",dataCSV.shape[0], " rows")
    df = dataCSV
    return df
