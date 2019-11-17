import datetime as dt
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import traphing.utils as ul
from traphing import Brain, test_storage_folder
from traphing.Brain._BacktestAnalysis import BacktestAnalysis
from traphing.data_classes import Portfolio, Velas
from traphing.graph.Gl import gl
from traphing.strategies import Coliseum, Trade
from traphing.strategies.entry import (CrossingMovingAverages,
                                       EarlySessionTrendFollower,
                                       EntryStrategy, WeeklyTriggerTimes)
from traphing.strategies.exit import ExitStrategy, StopLoss, TrailingStop
from traphing.utils import Timeframes, unwrap

print(os.path.abspath("./"))
plt.close("all")

folder_images = "./images/python_generated/strategies/"
storage_folder = test_storage_folder


"""
############################## Set up portfolio ##############################
"""
symbol_names_list = ["AUDCHF", "AUDCAD"]
timeframes_list = [Timeframes.M15, Timeframes.D1]
portfolio_name = "my_portfolio"

portfolio = Portfolio(portfolio_name, symbol_names_list, timeframes_list)
portfolio.load_data_from_csv(storage_folder)

start_time = dt.datetime(2019, 6, 20)
end_time = dt.datetime(2019, 8, 25)
portfolio.set_time_interval(start_time, end_time)

"""
############################## Set up strategies ##############################
"""
# First strategy
symbol_name = symbol_names_list[0]
timeframe = timeframes_list[0]
portfolio_params = {"symbol_names_list": [
    symbol_name], "timeframes_list": [timeframe]}
slow_MA_params = {"symbol_name": symbol_name,
                  "timeframe": timeframe, "indicator_name": "SMA", "args": {"n": 50}}
fast_MA_params = {"symbol_name": symbol_name,
                  "timeframe": timeframe, "indicator_name": "SMA", "args": {"n": 30}}
indicators_params = {"fast_MA": fast_MA_params, "slow_MA": slow_MA_params}
exit_strategy_params = {"class_name": "TrailingStop",
                        "params": {"indicators": {"stop_loss_pct": 0.1}}}
params = {"portfolio": portfolio_params,
          "indicators": indicators_params, "exit_strategy": exit_strategy_params}
entry_strategy1 = CrossingMovingAverages("Crossing averages", portfolio)
entry_strategy1.set_params(params)

# Second strategy
symbol_name = symbol_names_list[1]
timeframe = timeframes_list[0]
portfolio_params = {"symbol_names_list": [
    symbol_name], "timeframes_list": [timeframe]}
indicators_params = {"time": dt.time(2)}
exit_strategy_params = {"class_name": "ExitTime",
                        "params": {"indicators": {"time": dt.time(15)}}}
params = {"portfolio": portfolio_params,
          "indicators": indicators_params, "exit_strategy": exit_strategy_params}
entry_strategy2 = EarlySessionTrendFollower("ESTF", portfolio)
entry_strategy2.set_params(params)

coliseum = Coliseum()
coliseum.add_entry_strategy(entry_strategy1)
coliseum.add_entry_strategy(entry_strategy2)

"""
############################## Plot Strategy 1 ##############################
"""
entry_strategy_input = entry_strategy1.compute_input_series()
entry_strategy_triggers = entry_strategy1.compute_trigger_series()
entry_requests_queue = entry_strategy1.compute_requests_queue()

n_requests = entry_requests_queue.qsize()
entry_requests_dict = dict([entry_requests_queue.get()
                            for i in range(n_requests)])
entries_dates = sorted(list(entry_requests_dict.keys()))
indx_entry = 0
entry_request = entry_requests_dict[entries_dates[indx_entry]]

trade = Trade(name="my_trade12", request=entry_request,
              price=entry_request.price)
exit_strategy = entry_strategy1.create_exit_strategy(trade)

exit_strategy_input = exit_strategy.compute_input_series()
exit_strategy_triggers = exit_strategy.compute_trigger_series()
exit_requests_queue = exit_strategy.compute_requests_queue()
n_requests = exit_requests_queue.qsize()
exit_requests_dict = dict([exit_requests_queue.get()
                           for i in range(n_requests)])
exits_dates = sorted(list(exit_requests_dict.keys()))
#exit_request = exit_requests_dict[exits_dates[0]]

image_name = "entry_and_exit.png"
img_path = folder_images + image_name
gl.init_figure()
n_rows, n_cols = 4, 1
size_inches = [12, 8]
ax1 = gl.subplot2grid((n_rows, n_cols), (0, 0))
ax2 = gl.subplot2grid((n_rows, n_cols), (1, 0), sharex=ax1)
ax3 = gl.subplot2grid((n_rows, n_cols), (2, 0), sharex=ax1)
ax4 = gl.subplot2grid((n_rows, n_cols), (3, 0), sharex=ax1)

## Plot entry #####################
portfolio[symbol_names_list[0]][timeframes_list[0]].plot_barchart(
    axes=ax1, labels=["Entry and Exit strategies", "", "Entry signals"])

gl.plot(entry_strategy_input.index, entry_strategy_input,
        legend=list(entry_strategy_input.columns), axes=ax1)
gl.stem(entry_strategy_triggers.index,
        entry_strategy_triggers, axes=ax2, legend="Trades")

## Plot exit #############################
gl.plot(exit_strategy_input.index, exit_strategy_input, axes=ax3,
        legend=list(exit_strategy_input.columns), labels=["", "", "Exit signals"])
gl.stem(exit_strategy_triggers.index, exit_strategy_triggers,
        axes=ax4, legend="Exits", labels=["", "", "Exit requests"])

gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95,
                   wspace=.20, hspace=0, hide_xaxis=True)

"""
############################## Perform Backtesting ##############################
"""

brain = Brain(coliseum, portfolio, ul.BrainModes.BACKTEST_BATCH)

backtest_analysis = BacktestAnalysis(brain)
trade_analysis_df = backtest_analysis.backtest()

# backtest_analysis.print_summary()
# backtest_analysis.print_gains()


"""
PLOT strategy
"""
symbol_names_list_plot = symbol_names_list


size_inches = [12, 5]
gl.init_figure()
n_rows, n_cols = len(symbol_names_list_plot), 4

axes_list = [[], []]
ax1, ax2 = None, None

for i in range(n_rows):
    ax1 = gl.subplot2grid((n_rows, n_cols), (i, 0),
                          sharex=ax1, colspan=n_cols-1)
    ax2 = gl.subplot2grid((n_rows, n_cols), (i, n_cols-1),
                          sharex=ax2, sharey=ax2)
    ax2.yaxis.tick_right()

    symbol_name = symbol_names_list_plot[i]
    velas = portfolio[symbol_name][Timeframes.D1]

    velas.plot_barchart(axes=ax1, labels=["Trades performed", "", symbol_name])
    backtest_analysis.plot_trades(ax1, symbol_name)

    backtest_analysis.plot_return_duration_scatter(ax2, symbol_name)
    axes_list[0].append(ax1)
    axes_list[1].append(ax2)

gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95,
                   wspace=.10, hspace=0, hide_xaxis=True, axes_by_columns=axes_list)


# %%
