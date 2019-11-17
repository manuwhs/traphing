import datetime as dt

import numpy as np
import pandas as pd
import pytest

from traphing import test_storage_folder
from traphing.data_classes import Velas
from traphing.utils import Timeframes

# @pytest.fixture


def get_loaded_Velas():
    symbol_name = "AUDCHF"
    timeframe = Timeframes.M15
    storage_folder = test_storage_folder

    my_vela = Velas(symbol_name, timeframe)
    my_vela.load_data_from_csv(storage_folder)

    return my_vela


class TestVelasIndicators():

    def test_MAs(self):
        start_time = dt.datetime(2019, 7, 20)
        end_time = dt.datetime(2019, 8, 20)
        velas = get_loaded_Velas()
        velas.set_time_interval(start_time, end_time)

        indicators_name = ["SMA", "EMA", "WMA", "HMA", "HMAg"]
        indicators_args = [{"n": 20, "series_name": "Close"}, {"n": 40}, {"n": 40},
                           {"n": 40}, {"n": 40}]

        for i in range(len(indicators_name)):
            name = indicators_name[i]
            args = indicators_args[i]

            if(name == "HMAg"):
                n_nan = args["n"] - 1 + int(np.sqrt(args["n"])) - 1
            elif(name == "HMA"):
                n_nan = args["n"] - 1 + int(np.sqrt(args["n"])) - 1
            else:
                n_nan = args["n"] - 1

            indicator_output = velas.indicator(name, **args)

            assert indicator_output.shape == (velas.df.shape[0],)
            assert isinstance(indicator_output, pd.Series)
            assert np.mean(np.isnan(indicator_output.values[:n_nan-1])) == 1
            assert np.mean(np.isnan(indicator_output.values[n_nan:])) == 0
            assert indicator_output.index[0] == velas.df.index[0]
