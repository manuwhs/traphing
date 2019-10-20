import sys
sys.path.insert(0,"..") # Adds higher directory to python modules path.
from traphing.data_classes import Portfolio
from traphing.utils import Timeframes
import pytest
import datetime as dt
import pandas as pd

# @pytest.fixture
def get_loaded_Portfolio():
    storage_folder = "./data/storage/"
    
    portfolio_id = "hello"
    symbol_names_list = ["AUDCHF", "AUDCAD"]
    timeframes_list = [Timeframes.M15, Timeframes.D1]
    
    my_portfolio = Portfolio(portfolio_id, symbol_names_list, timeframes_list)
        
    my_portfolio.load_data_from_csv(storage_folder)
    return my_portfolio

class TestPortfolio():
    
    def test_initialization_parameters(self):
        """ Basic initialization parameters 
        """
        portfolio_id = "hello"
        symbol_names_list = ["AUDCHF", "AUDCAD"]
        timeframes_list = [Timeframes.M15, Timeframes.D1]
        
        my_portfolio = Portfolio(portfolio_id, symbol_names_list, timeframes_list)
        
        assert symbol_names_list == my_portfolio.symbol_names_list
        assert timeframes_list == my_portfolio[symbol_names_list[0]].timeframes_list
    

    def test_add_del_symbols(self):
        """ Basic initialization parameters 
        """
        portfolio_id = "hello"
        symbol_names_list = ["AUDCHF", "AUDCAD"]
        timeframes_list = [Timeframes.M15, Timeframes.D1]
        
        my_portfolio = Portfolio(portfolio_id, symbol_names_list, timeframes_list)
        my_portfolio.add_symbol("Caca", [])
        assert my_portfolio.symbol_names_list == ["AUDCHF", "AUDCAD", "Caca"]
        
        my_portfolio.del_symbol("AUDCHF")
        my_portfolio.del_symbol("Caca")
        assert my_portfolio.symbol_names_list == ["AUDCAD"]
        
        my_portfolio.add_symbol("Caca", [])
        assert my_portfolio.symbol_names_list == [ "AUDCAD", "Caca"]
        
        
    def test_load_data_from_csv(self):
        my_portfolio = get_loaded_Portfolio()
        for symbol_name in my_portfolio.symbol_names_list:
            if (symbol_name == "AUDCHF"):
                assert my_portfolio[symbol_name][Timeframes.M15].df.shape == (100400,5)
                assert my_portfolio[symbol_name][Timeframes.D1].df.shape  == (4894,5)
            elif(symbol_name == "AUDCAD"):
                assert my_portfolio[symbol_name][Timeframes.M15].df.shape == (99483,5)
                assert my_portfolio[symbol_name][Timeframes.D1].df.shape  == (4963,5)
        
        
