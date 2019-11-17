from typing import List

import pandas as pd

from ..graph.Gl import gl
from ..strategies import Trade
from ..strategies.exit import ExitTradeRequest
from . import Brain, ClosedTradeAnalysis


class BacktestAnalysis:
    """Class that performs the analysis of a given backtest using the
     open_trades_dict and closed_trades_pairs_dict from a Brain object.
    """

    def __init__(self, brain: Brain):
        self.brain = brain

    def backtest(self) -> pd.DataFrame:
        """Calls the brain's backtest function and computes the analysis
        of the trades into a pd.DataFrame that it returns
        """
        self.brain.backtest()
        self.trade_analysis_list = self.get_trade_analysis_list()
        self.trade_analysis_df = self.get_trade_analysis_df()
        return self.trade_analysis_df

    def get_trade_analysis_list(self) -> List[ClosedTradeAnalysis]:
        """Creates the ClosedTradeAnalysis object for every closed and open trade.
        """
        trade_analysis_list = []
        for closed_trade_name in list(self.brain.closed_trades_pairs_dict.keys()):
            entry_trade, exit_trade = self.brain.closed_trades_pairs_dict[closed_trade_name]
            trade_analysis = ClosedTradeAnalysis(entry_trade, exit_trade)
            trade_analysis_list.append(trade_analysis)

        for open_trade_name in list(self.brain.open_trades_dict.keys()):
            entry_trade = self.brain.open_trades_dict[open_trade_name]
            trade_analysis = ClosedTradeAnalysis.from_open_trade(
                entry_trade, self.brain.portfolio)
            trade_analysis_list.append(trade_analysis)
        return trade_analysis_list

    def get_trade_analysis_df(self) -> pd.DataFrame:
        """Creates a pandas Dataframe with the information of all closed and open trades
        from the trade_analysis_list
        """
        rows = ["entry_name", "exit_name", "symbol_name", "gain", "duration", "entry_price", "exit_price",
                "entry_timestamp", "exit_timestamp", "ret", "faked_exit_trade"]
        data_dict = {}
        for row in rows:
            data_dict[row] = [getattr(trade_analysis, row)
                              for trade_analysis in self.trade_analysis_list]

        data_dict["list_index"] = range(len(data_dict[rows[0]]))
        df = pd.DataFrame(data_dict)
        df.set_index("entry_name", inplace=True)
        df.sort_values(by=['entry_timestamp'])
        return df

    """
    ############ Methods over all the trades ################
    """

    def print_gains(self):
        """Simply prints the information about the trades"""
        for trade_analysis in self.trade_analysis_list:
            trade_analysis.print_summary()

    def plot_trades(self, axes=None, symbol_name: str = None):
        """Plots the trade lines. It allows to filter by symbol_name.
        """
        df = self.trade_analysis_df
        if (symbol_name is not None):
            df = df[df["symbol_name"] == symbol_name]

#        df_positive_closed = df[df["gain"] >0 & df["fake_exit_trade"] == False]
#
#        gl.plot([self.entry_timestamp, self.exit_timestamp],[self.entry_price, self.exit_price], axes = axes,
#                legend = [], ls = ls, lw = 1, alpha = 0.5, color = color)

        indexes = df["list_index"]
        for i in indexes:
            trade_analysis = self.trade_analysis_list[i]
            trade_analysis.plot_trade_line(axes)

    def plot_return_duration_scatter(self, axes=None, symbol_name: str = None):
        """Plots a scatter plot return-duration of the trades.
        It allows to filter by symbol_name.
        """
        df = self.trade_analysis_df
        if (symbol_name is not None):
            df = df[df["symbol_name"] == symbol_name]

        df_aux = df[df["gain"] < 0]
        color = "r"
        gl.scatter(df_aux["duration"].map(pd.Timedelta.total_seconds)/(60*1440), df_aux["ret"],
                   labels=["Return - duration", "duration(days)", "return(%)"], axes=axes, color=color, alpha=0.5)

        df_aux = df[df["gain"] >= 0]
        color = "b"
        gl.scatter(df_aux["duration"].map(pd.Timedelta.total_seconds)/(60*1440), df_aux["ret"],
                   labels=["Return - duration", "duration(days)", "return(%)"], axes=axes, color=color, alpha=0.5)
