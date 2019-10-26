import numpy  
import pandas as pd  
import math as m
from ... import indicators
from typing import List

from ... import utils as ul
"""
This library should only include indicators that need more than one timeframe.
"""

def forex_cycle(portfolio, timeframe, currencies: List[str]):
    """This indicator computes the exchange cycle between the currencies given
       It first checks if the cycle can be computes with the available forex data
       Then it computes the cycle 
    """
    
    df = portfolio.map_timeframe(timeframe, "series", name = "Open")
    
    symbol_names_list = list(df.columns)
    exchanges = ul.get_exchange_cycle(currencies, symbol_names_list)
    forex_cycle = 1
    for symbol_name in exchanges:
        if (symbol_name in symbol_names_list):
            exchange = df[symbol_name]
        else:
            exchange = 1/df[ul.reverse_forex_name(symbol_name)]
            print(ul.reverse_forex_name(symbol_name))
        forex_cycle = exchange * forex_cycle
    
    forex_cycle.name = "_".join(currencies)
    return forex_cycle