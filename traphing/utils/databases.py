import pandas as pd
from .. import utils
from ..utils import Timeframes

"""
############## CSV related functions ################################
"""
def get_relative_csv_file_path(symbol_name: str, timeframe: Timeframes):
    """ Generates the filename convention of the csv"""
    timeframe_name = timeframe.name
    file_path =  timeframe_name + "/" + \
            symbol_name + "_" + timeframe_name + ".csv"
    return file_path


def load_data_from_csv(symbol_name, timeframe, 
                       storage_folder = "./storage/", verbose = 0):
    """This function loads the data from the file  file_dir + file_name if file_name is provided
    Otherwise it uses the naming convention to find it from the root folder:
    The file must have the path:  ./TimeScale/symbolName_TimeScale.csv
    
    If we did not specify the symbolID or period and we set them in the 
    initialization it will get them from there
    specific and adds its values to the main structure
    """
    whole_path = storage_folder + get_relative_csv_file_path(symbol_name, timeframe)
    try:
        data_csv = pd.read_csv(whole_path, sep = ',', index_col = 0, header = 0)
        processed_dates = pd.to_datetime(data_csv.index)
        data_csv.index = processed_dates
        # Dealing with legacy when we named the index as Dates
        if (data_csv.index.name == "Date"):
            data_csv.index.name = "Timestamp"
    except IOError:
        error_msg = "File does not exist: " + whole_path 
        print (error_msg)
        data_csv = utils.get_empty_df()
    if(verbose):
        print ("Size " + whole_path +": ",data_csv.shape[0], " rows")
    return data_csv
