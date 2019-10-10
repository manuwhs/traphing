import sys
import datetime as dt
sys.path.append("..") # Adds higher directory to python modules path.

from traphing.data_classes import Velas
import pandas as pd
import sys
from traphing.utils import Timeframes
from traphing.utils import unwrap

import matplotlib.pyplot as plt 
plt.close("all")

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

start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,8,20)
my_vela.set_time_interval(start_time, end_time)
        

timestamps = my_vela.timestamps
close_values = my_vela["Close"]

from traphing.graph.Gl import gl
gl.plot(timestamps,close_values, legend = ["Hello"])
#gl.init_figure()

#my_vela.plot_series()
#my_vela.plot_barchart()
#my_vela.plot_candlesticks()

class caca():
    def __init__(self):
        self.my_int = 1
        self.my_float = 1.1
        self.my_str = "d"
        self.my_list = [1,2]
        self.my_tuple = (3,4)
        self.my_dict = {"one":1,"two":2}
        self.my_complex = [1,{"one":1,"two":2}]
        
my_caca = caca()


        
unwrap(my_vela, "my_caca")







