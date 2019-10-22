import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

import sys
sys.path.insert(0, "..")  # Adds higher directory to python modules path.
from traphing.Brain._BacktestAnalysis import BacktestAnalysis

from traphing.data_classes import Velas, Portfolio
from traphing import Brain
from traphing.strategies import Trade, Coliseum
from traphing.strategies.entry import EntryStrategy, CrossingMovingAverages
from traphing.strategies.exit import ExitStrategy, StopLoss

from traphing.utils import Timeframes, unwrap
import traphing.utils  as ul

from traphing.graph.Gl import gl

folder_images = "./images/python_generated/strategies/"
plt.close("all")
"""
############################## Set up portfolio ##############################
"""
symbol_names_list = ["AUDCHF", "AUDCAD"]
timeframes_list = [Timeframes.M15, Timeframes.D1]
portfolio_name = "my_portfolio"

storage_folder = "../tests/data/storage/"

portfolio = Portfolio(portfolio_name, symbol_names_list, timeframes_list)
portfolio.load_data_from_csv(storage_folder)

start_time = dt.datetime(2019,8,20); end_time = dt.datetime(2019,9,25)
portfolio.set_time_interval(start_time,end_time)

"""
############################## Set up strategies ##############################
"""

# First entry strategy
timeframe = timeframes_list[0]
symbol_name = symbol_names_list[0]
entry_strategy1 = CrossingMovingAverages("CMA_%s_%s"%(symbol_name,timeframe.name), portfolio)
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":45}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":20}}
entry_strategy1.set_params({"fast_MA": fast_MA_params, "slow_MA": slow_MA_params})

# Second entry strategy
timeframe = timeframes_list[0]
symbol_name = symbol_names_list[1]
entry_strategy2 = CrossingMovingAverages("CMA_%s_%s"%(symbol_name,timeframe.name), portfolio)
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":45}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":20}}
entry_strategy2.set_params({"fast_MA": fast_MA_params, "slow_MA": slow_MA_params})

coliseum = Coliseum()
coliseum.add_entry_strategy(entry_strategy1)
coliseum.add_entry_strategy(entry_strategy2)

"""
############################## Set up strategies ##############################
"""

brain = Brain(coliseum, portfolio, ul.BrainModes.BACKTEST_BATCH)

backtest_analysis = BacktestAnalysis(brain)
trade_analysis_df = backtest_analysis.backtest()

#backtest_analysis.print_summary()
#backtest_analysis.print_gains()


"""
PLOT strategy
"""
symbol_names_list_plot = symbol_names_list


size_inches = [12, 5]
gl.init_figure()
n_rows, n_cols = len(symbol_names_list_plot),4

axes_list = [[],[]]
ax1, ax2 = None, None

for i in range (n_rows):
    ax1 = gl.subplot2grid((n_rows, n_cols),(i,0), sharex = ax1, colspan = n_cols-1)
    ax2 = gl.subplot2grid((n_rows, n_cols),(i,n_cols-1), sharex = ax2, sharey = ax2)
    ax2.yaxis.tick_right()
    
    symbol_name = symbol_names_list_plot[i]
    velas = portfolio[symbol_name][Timeframes.D1]
    
    velas.plot_barchart(axes = ax1, labels = ["Trades performed","",symbol_name])
    backtest_analysis.plot_trades(ax1, symbol_name)
    
    backtest_analysis.plot_return_duration_scatter(ax2, symbol_name)
    axes_list[0].append(ax1); axes_list[1].append(ax2)

gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.10, hspace=0, hide_xaxis = True, axes_by_columns = axes_list)

