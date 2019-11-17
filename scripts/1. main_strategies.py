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
from traphing.strategies.entry import CrossingMovingAverages,EarlySessionTrendFollower,WeeklyTriggerTimes
from traphing.graph.Gl import gl

import matplotlib.pyplot as plt 
plt.close("all")

portfolio_name = "Manu's shit"
symbol_names = ["AUDCHF","AUDCAD"]
timeframes = [Timeframes.M15, Timeframes.D1]
storage_folder = "../tests/data/storage/"

portfolio = Portfolio(portfolio_name, symbol_names, timeframes)
portfolio.load_data_from_csv(storage_folder)

start_time = dt.datetime(2019,7,10); end_time = dt.datetime(2019,7,25)
portfolio.set_time_interval(start_time,end_time)
"""
###################################### REAL STRATEGY STU
"""


if(1):
    # Initialize
    entry_strategy = CrossingMovingAverages("Crossing averages", portfolio)
    symbol_name = symbol_names[0]
    timeframe = timeframes[0]
    
    portfolio_params = {"symbol_names":[symbol_name], "timeframes":[timeframe]}
    slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":50}}
    fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":30}}
    indicators_params = {"fast_MA": fast_MA_params, "slow_MA": slow_MA_params}
    exit_strategy_params = {"class_name":"TrailingStop",
                            "params":{"indicators":{"stop_loss_pct":0.1}}}
if(0):
    # Initialize
    entry_strategy = EarlySessionTrendFollower("ESTF", portfolio)
    # Set the paramters
    symbol_name = symbol_names[0]
    timeframe = timeframes[0]
    
    portfolio_params = {"symbol_names":[symbol_name], "timeframes":[timeframe]}
    indicators_params = {"time":dt.time(2)}
    exit_strategy_params = {"class_name":"ExitTime",
                            "params":{"indicators":{"time":dt.time(15)}}}

if(0):
    # Initialize
    entry_strategy = WeeklyTriggerTimes("WTT", portfolio)
    # Set the paramters
    symbol_name = symbol_names[0]
    timeframe = timeframes[0]
    
    portfolio_params = {"symbol_names":[symbol_name], "timeframes":[timeframe]}
    indicators_params = {"weekdays_list":[0,2,4], 
                      "times_list":[dt.time(4,0,0),dt.time(12,0,0)]}
    exit_strategy_params = {"class_name":"ExitTime",
                            "params":{"indicators":{"time":dt.time(15)}}}
    
params = {"portfolio": portfolio_params, "indicators": indicators_params, "exit_strategy":exit_strategy_params}
entry_strategy.set_params(params)


# Compute the signals
entry_strategy_series = entry_strategy.compute_input_series()
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
exit_strategy = entry_strategy.create_exit_strategy(trade)

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
  ############## PLOTTING ###############
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
gl.stem(entry_strategy_series.index,entry_trigger_series, axes = ax2, legend = "Trades")

## Plot exit
gl.plot(exit_strategy_series.index, exit_strategy_series, axes = ax3, 
        legend = list(exit_strategy_series.columns), labels = ["", "", "Exit signals"])
gl.stem(exit_series.index,exit_series, axes = ax4, legend = "Exits", labels = ["", "", "Exit requests"])

gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)