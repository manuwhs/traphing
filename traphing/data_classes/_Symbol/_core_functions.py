import copy
import numpy as np
import pandas as pd

from ...data_classes import Velas
from ...utils import Timeframes


########### Initialization functions ##############
def _init_velas(self, timeframes):
    for timeframe in timeframes:
        self.add_velas(timeframe)


######################## Interface functions to velas ###############
def add_velas(self, timeframe: Timeframes, velas: Velas = None):
    if velas is None:
        velas = Velas(self.symbol_name, timeframe)
    self._velas_dict[timeframe] = velas


def del_velas(self, timeframe: Timeframes):
    del self._velas_dict[timeframe]


def del_all_velas(self):
    self._velas_dict = {}

######## Functions to apply to all timeDatas #################


def set_time_interval(self, start_time=None, end_time=None, trim=False):
    for timeframe in self.timeframes:
        self[timeframe].set_time_interval(start_time, end_time, trim=trim)

    self.start_time = start_time
    self.end_time = end_time

########### Other symbol functions #############


def get_candlestick(self, datetime):
    """
    Gets the last candlesick that comes before the provided datetime.
    """
    candlesticks = []
    # TODO: Change logic with this line?
    # timeframe =self.timeframes[np.argmin(x.value for x in self.timeframes)]
    for timeframe in self.timeframes:
        row = self[timeframe].get_candlestick(datetime)
        candlesticks.append(row)
    df = pd.concat(candlesticks, axis=0)

    return df.loc[[max(df.index)]]


def load_properties_from_df(self, df):
    self.properties.load_properties_from_df(df)


def estimate_market_hours(self, timeframe=None):
    """This function estimates the properties of the market hours objects by calling the
    estimation of dict days.
    """
    if timeframe is None:
        timeframe = self.timeframes[np.argmin(
            x.value for x in self.timeframes)]
    timestamps = self[timeframe].timestamps

    self.market_hours.estimate_special_trading_days_from_timestamps(timestamps, open_time=None,
                                                                    close_time=None,  timeframe=timeframe, trading_days_list=None)


def get_subsymbol(self, timeframes=None):
    """Returns a subsymbol with just some of the timeframes
    """

    if(timeframes is None):
        timeframes = self.timeframes

    subsymbol = copy.copy(self)
    subsymbol.del_all_velas()

    for timeframe in timeframes:
        subsymbol.add_velas(timeframe, self[timeframe])

    return subsymbol
