import sys
sys.path.append("..") # Adds higher directory to python modules path.

import traphing.data_classes.Velas as Velas
import pandas as pd
import sys
from traphing.utils import Timeframes

symbol_name = "EUR"
timeframe = Timeframes.M15

my_vela = Velas(symbol_name, timeframe)

symbol_name = "AUDCHF"
timeframe = Timeframes.M15
storage_folder = "../tests/data/storage/"

my_vela = Velas(symbol_name, timeframe)
my_vela.load_data_from_csv(storage_folder)

options = ["Open","Close","High","Low","Volume","Average", "RangeHL","RangeCO"]

for name in options:
    time_series_data = my_vela.series(name)
    print (name, ": ", type(time_series_data))
    assert time_series_data.shape == (my_vela.df.shape[0],)
    assert isinstance(time_series_data, pd.Series)
