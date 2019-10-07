""" Library containing all the data structures

"""
import pandas as pd
from enum import Enum
import datetime as dt
import numpy as np

# Define the empty dataframe structure
keys = ['Open', 'High', 'Low', 'Close', 'Volume']

def get_empty_df():
    df = pd.DataFrame(None,columns = keys)
    df.index.name = "Timestamp"
    return df

def is_velas_df(df):
    """ Checks if the given DataFrame follows the convention of Velas.df
    """
    empty_df = get_empty_df()
    
    if sorted(list(empty_df.columns)) != sorted(list(df.columns)):
        return False
    if empty_df.index.name != df.index.name:
        return False
    return True
    
keys_col = ['Symbol','Type','Size','TimeOpen','PriceOpen', 'Comision','CurrentPrice','Profit']
empty_coliseum = pd.DataFrame(None,columns = keys_col )


# Dictionary between period names and value
periods = [1,5,15,30,60,240,1440,10080,43200, 43200*12]
periods_names = ["M1","M5","M15","M30","H1","H4","D1","W1","W4","Y1"]


period_dic = dict(zip(periods,periods_names))
names_dic = dict(zip(periods_names, periods))

class Timeframes(Enum):
    M1 = 0
    M5 = 1
    M15 = 2
    M30 = 3
    H1 = 4
    H4 = 5
    D1 = 6
    W1 = 7
    W4 = 8
    Y1 = 9

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def get_foldersData(source = "FxPro", rrf = "../" ):
    # Returns the folders where we can find the previously stored data,
    # new data to download and the info about the symbols we have or 
    # want to download.
#    rrf = "../" # relative_root_folder

    if (source == "Hanseatic"):
        storage_folder = rrf + "./storage/Hanseatic/"
        updates_folder = rrf +"../Hanseatic/MQL4/Files/"
            
    elif (source == "MQL5"):
        storage_folder = rrf + "./storage/MQL5/"
        updates_folder = rrf +"./MT5/MQL5/MQL5/Files/"
            
    elif (source == "Yahoo"):
        storage_folder = rrf +"./storage/Yahoo/"
        updates_folder = rrf +"internet"
        
    elif (source == "Google"):
        storage_folder = rrf +"./storage/Google/"
        updates_folder = rrf +"internet"

    else:
        print ("Not recognized")
    return storage_folder, updates_folder


    
    

        