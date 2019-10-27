import datetime as dt
import sys
import numpy as np

sys.path.insert(0, "..")  # Adds higher directory to python modules path.

from traphing.data_classes import Velas, Portfolio, Symbol
import pandas as pd
import sys
from traphing.utils import Timeframes
from traphing.utils import unwrap
import traphing.utils  as ul
from traphing.strategies import Trade
from traphing.strategies.exit import StopLoss
from traphing.strategies.entry import EntryStrategy
from traphing.graph.Gl import gl

import matplotlib.pyplot as plt 
plt.close("all")

load_data = 0

if (load_data):
    portfolio_name = "Manu's shit"
    timeframes_list = [Timeframes.M15, Timeframes.D1]
    dataSource =  "MQL5"  # Hanseatic  FxPro GCI Yahoo
    [storage_folder, updates_folder] = ul.get_foldersData(source = dataSource, rrf = "../../../" )
    symbols_info_csv = Symbol.load_symbols_properties_csv(storage_folder)
    
    symbol_names_list = list(symbols_info_csv.index)
    all_portfolio = Portfolio(portfolio_name, symbol_names_list, timeframes_list)
    all_portfolio.load_data_from_csv(storage_folder)

    start_time = dt.datetime(2019,7,22); end_time = dt.datetime(2019,7,25)
    all_portfolio.set_time_interval(start_time,end_time)


symbol_names_list = list(symbols_info_csv.index)

currency = "GBP"
currencies_list = ["EUR","USD","DKK","GBP","AUD","CHF"]
currencies_list = ['EUR', 'CHF', 'GBP']

#symbol_names_list = all_portfolio.get_related_forex_currencies(currency)
#print (symbol_names_list)
portfolio = all_portfolio.get_subportfolio(symbol_names_list )

symbol_names_list = portfolio.get_non_empty(timeframes_list[0])
portfolio = all_portfolio.get_subportfolio(symbol_names_list )

print (symbol_names_list)
portfolio.estimate_symbols_market_hours(timeframes_list[0])
symbol_names_list = portfolio.get_currencies_with_market_hours(open_time = dt.time(0), close_time = dt.time(0))

print (symbol_names_list)
portfolio = portfolio.get_subportfolio(symbol_names_list)

start_time = dt.datetime(2019,7,9); end_time = dt.datetime(2019,7,25)
portfolio.set_time_interval(start_time,end_time)

if 0:
    gl.init_figure()
    nrows = len(symbol_names_list) 
    
    i = 0; axes = None
    for symbol_name in symbol_names_list:
        axes = gl.subplot2grid((nrows,1),(i,0),sharex = axes)
        portfolio[symbol_name][timeframes_list[0]].plot_series(axes = axes, series_name = "Close", labels = ["","",symbol_name])
        i+=1 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)


indicators_df = portfolio.map_timeframe(timeframes_list[0], "series", name = "Open")
indicators_df["mean"] = indicators_df.mean(axis = 1)

symbol_names_list = indicators_df.columns
currencies = ["EUR","USD","AUD"]

forex_cycle = portfolio.indicator(name = "forex_cycle", timeframe  = timeframes_list[0], currencies = currencies)

gl.plot(indicators_df.index, forex_cycle, legend = [forex_cycle.name], labels = ["Forex cycle","",forex_cycle.name])
