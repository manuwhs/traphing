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
symbol_names_list = ["AUDCHF"]
timeframes_list = [Timeframes.M15]
portfolio_name = "my_portfolio"

storage_folder = "../tests/data/storage/"

portfolio = Portfolio(portfolio_name, symbol_names_list, timeframes_list)
portfolio.load_data_from_csv(storage_folder)

start_time = dt.datetime(2019,7,20); end_time = dt.datetime(2019,7,25)
portfolio.set_time_interval(start_time,end_time)

"""
############################## Set up strategies ##############################
"""
timeframe = timeframes_list[0]
symbol_name = symbol_names_list[0]
# First entry strategy
entry_strategy1 = CrossingMovingAverages("Crossing averages 1", portfolio)
symbol_name = symbol_names_list[0]
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":45}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":20}}
entry_strategy1.set_slow_MA(slow_MA_params)
entry_strategy1.set_fast_MA(fast_MA_params)

# Second entry strategy
entry_strategy2 = CrossingMovingAverages("Crossing averages 2", portfolio)
slow_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args": {"n":40}}
fast_MA_params = {"symbol_name":symbol_name,"timeframe": timeframe,"indicator_name":"SMA", "args":{"n":10}}
entry_strategy2.set_slow_MA(slow_MA_params)
entry_strategy2.set_fast_MA(fast_MA_params)

coliseum = Coliseum()
coliseum.add_entry_strategy(entry_strategy1)
coliseum.add_entry_strategy(entry_strategy2)

"""
############################## Set up strategies ##############################
"""

brain = Brain(coliseum, portfolio)
#brain.backtest()

backtest_analysis = BacktestAnalysis(brain)
backtest_analysis.backtest()
backtest_analysis.print_gains()

velas = portfolio[symbol_name][timeframe]
gl.init_figure()
velas.plot_barchart()

backtest_analysis.plot_trades()
backtest_analysis.print_summary()