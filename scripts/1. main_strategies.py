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
from traphing.strategies import Trade
from traphing.strategies.exit import StopLoss
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
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":50}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":30}}

entry_strategy.set_slow_MA(slow_MA_params)
entry_strategy.set_fast_MA(fast_MA_params)

# Compute the signals
entry_strategy_series = entry_strategy.compute_input_series()
slow_MA = entry_strategy_series["slow_MA"]
fast_MA = entry_strategy_series["fast_MA"]
entry_trigger_series = entry_strategy.compute_trigger_series()

# Compute the BUYSELL Requests
entry_requests_queue = entry_strategy.compute_requests_queue()
n_requests = entry_requests_queue.qsize()
entry_requests_dict = dict([entry_requests_queue.get() for i in range(n_requests)])
entries_dates = sorted(list(entry_requests_dict.keys()))
if len(entries_dates):    
    entry_request = entry_requests_dict[entries_dates[0]]

# Compute Trade
trade = Trade(name = "my_trade12", request = entry_request,
                 price = entry_request.price)

### Exit strategy
exit_strategy =  StopLoss(name = "Exit coward", trade = trade, portfolio = portfolio)
# Set the velas it will be listening to.
exit_strategy.set_velas(symbol_name, timeframe)
exit_strategy.set_stop_loss(pct = 0.1)
#exit_strategy.set_stop_loss(price = 0.8)
# Get shit
exit_strategy_series = exit_strategy.compute_input_series()
exit_series= exit_strategy.compute_trigger_series()

# Compute the BUYSELL Requests
exit_requests_queue = exit_strategy.compute_requests_queue()
n_requests = exit_requests_queue.qsize()
exit_requests_dict = dict([exit_requests_queue.get() for i in range(n_requests)])
exits_dates = sorted(list(exit_requests_dict.keys()))
if len(exits_dates):    
    exit_request = exit_requests_dict[exits_dates[0]]


"""
  ##############3 PLOTTING ###############
"""

## Plot the EntryPoints of the strategy
gl.init_figure()
n_rows, n_cols = 4,1; size_inches = [12, 5]
ax1 = gl.subplot2grid((n_rows, n_cols),(0,0))
ax2 = gl.subplot2grid((n_rows, n_cols),(1,0), sharex = ax1)
ax3 = gl.subplot2grid((n_rows, n_cols),(2,0), sharex = ax1)
ax4 = gl.subplot2grid((n_rows, n_cols),(3,0), sharex = ax1)

portfolio[symbol_name][timeframe].plot_barchart(axes = ax1, labels = ["Entry and Exit strategies", "", "Entry signals"])
gl.plot(entry_strategy_series.index, entry_strategy_series, legend = list(entry_strategy_series.columns), axes =ax1)

difference = fast_MA - slow_MA
normalized_difference = difference/np.max(np.abs((difference)))
gl.fill_between(entry_strategy_series.index, normalized_difference, 
                labels = ["", "", "Entry requests"], legend = "Normalized signal diff", axes =ax2)
gl.stem(entry_strategy_series.index,entry_trigger_series, axes = ax2, legend = "Trades")

## Plot exit
gl.plot(exit_strategy_series.index, exit_strategy_series, axes = ax3, 
        legend = list(exit_strategy_series.columns), labels = ["", "", "Exit signals"])

difference = exit_strategy_series["Close"] - exit_strategy_series["Stop_loss"]
normalized_difference = difference/np.max(np.abs((difference)))
gl.fill_between(exit_strategy_series.index, normalized_difference, legend = ["Normalized signal diff"], axes =ax4)
gl.stem(exit_series.index,exit_series, axes = ax4, legend = "Exits", labels = ["", "", "Exit requests"])

gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)