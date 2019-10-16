import datetime as dt
import sys
import numpy as np

sys.path.insert(0, "..")  # Adds higher directory to python modules path.

from traphing.data_classes import Velas, Portfolio
import pandas as pd
import sys
from traphing.utils import Timeframes
from traphing.utils import unwrap
import traphing.utils  as ul
from traphing.strategies.entry import CrossingMovingAverages
from traphing.graph.Gl import gl

import matplotlib.pyplot as plt 
plt.close("all")

portfolio_name = "Manu's shit"
symbol_names_list = ["AUDCHF"]
timeframes_list = [Timeframes.M15]
storage_folder = "../tests/data/storage/"

portfolio = Portfolio(portfolio_name, symbol_names_list, timeframes_list)
portfolio.load_data_from_csv(storage_folder)

start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,7,25)
portfolio.set_time_interval(start_time,end_time)
"""
###################################### REAL STRATEGY STU
"""

symbol_name = symbol_names_list[0]
timeframe = timeframes_list[0]

# Initialize
entry_strategy = CrossingMovingAverages("Crossing averages 1", portfolio)

# Set the paramters
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":40}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":20}}

entry_strategy.set_slow_MA(slow_MA_params)
entry_strategy.set_fast_MA(fast_MA_params)

# Compute the signals
signals = entry_strategy.compute_signals()
slow_MA = signals["slow_MA"]
fast_MA = signals["fast_MA"]
# Compute the BUYSELL signals
trade_signals = entry_strategy.compute_trade_signals()

## Plot the EntryPoints of the strategy
gl.init_figure()
ax1 = gl.subplot2grid((2,1),(0,0))
ax2 = gl.subplot2grid((2,1),(1,0), sharex = ax1)

portfolio[symbol_name][timeframe].plot_barchart(axes = ax1)
gl.plot(signals.index, signals, legend = list(signals.columns), axes =ax1)

normalized_difference = (slow_MA - fast_MA)/np.max(np.abs((slow_MA - fast_MA)))
gl.fill_between(signals.index, normalized_difference, legend = ["Normalized diff"], axes =ax2)
gl.stem(signals.index,trade_signals, axes = ax2, legend = "Trades")


