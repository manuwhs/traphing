from traphing.data_classes import Portfolio
from traphing.utils import Timeframes
from traphing import test_storage_folder, test_storage_folder2
import pytest
import datetime as dt
import pandas as pd

# @pytest.fixture


def get_loaded_Portfolio():
    storage_folder = test_storage_folder

    portfolio_id = "hello"
    symbol_names = ["AUDCHF", "AUDCAD"]
    timeframes = [Timeframes.M15, Timeframes.D1]

    my_portfolio = Portfolio(portfolio_id, symbol_names, timeframes)

    my_portfolio.load_data_from_csv(storage_folder)
    return my_portfolio


class TestPortfolio():

    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        portfolio_id = "hello"
        symbol_names = ["AUDCHF", "AUDCAD"]
        timeframes = [Timeframes.M15, Timeframes.D1]

        my_portfolio = Portfolio(portfolio_id, symbol_names, timeframes)

        assert symbol_names == my_portfolio.symbol_names
        assert timeframes == my_portfolio[symbol_names[0]].timeframes

    def test_add_del_symbols(self):
        """ Basic initialization parameters 
        """
        portfolio_id = "hello"
        symbol_names = ["AUDCHF", "AUDCAD"]
        timeframes = [Timeframes.M15, Timeframes.D1]

        my_portfolio = Portfolio(portfolio_id, symbol_names, timeframes)
        my_portfolio.add_symbol("Caca", [])
        assert my_portfolio.symbol_names == ["AUDCHF", "AUDCAD", "Caca"]

        my_portfolio.del_symbol("AUDCHF")
        my_portfolio.del_symbol("Caca")
        assert my_portfolio.symbol_names == ["AUDCAD"]

        my_portfolio.add_symbol("Caca", [])
        assert my_portfolio.symbol_names == ["AUDCAD", "Caca"]

    def test_load_data_from_csv(self):
        my_portfolio = get_loaded_Portfolio()
        for symbol_name in my_portfolio.symbol_names:
            if (symbol_name == "AUDCHF"):
                assert my_portfolio[symbol_name][Timeframes.M15].df.shape == (
                    100400, 5)
                assert my_portfolio[symbol_name][Timeframes.D1].df.shape == (
                    4894, 5)
            elif(symbol_name == "AUDCAD"):
                assert my_portfolio[symbol_name][Timeframes.M15].df.shape == (
                    99483, 5)
                assert my_portfolio[symbol_name][Timeframes.D1].df.shape == (
                    4963, 5)
