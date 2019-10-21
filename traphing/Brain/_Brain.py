import pandas as pd
import numpy as np

import datetime as dt

from ..strategies import Trade, Coliseum
from ..strategies.entry import EntryRequest
from ..strategies.exit import ExitRequest, StopLoss
from ..utils import unwrap

class Brain:
    def __init__(self, coliseum, portfolio):
        self.coliseum = coliseum
        self.money_management = None
        self.portfolio = portfolio

        self.trade_counter = 0
        
        self.open_trades_dict = dict()
        self.closed_trades_pairs_dict = dict()
        
    def make_trade(self, request):
        """
        Makes the trade
        """
        trade = Trade(trade_id = "trade_" + str(self.trade_counter), request = request,
             trade_price = request.price, trade_timestamp = dt.datetime.now())
        
        self._log_trade(trade)
        return trade
    
    def _log_trade(self, trade):
        """
        It logs the performed trade.
        """
        if isinstance(trade.request, EntryRequest):
            self.open_trades_dict[trade.request.entry_request_id] = trade
            
        elif isinstance(trade.request, ExitRequest):
            self.closed_trades_pairs_dict[trade.request.entry_request_id] = [self.open_trades_dict[trade.request.entry_request_id], trade]
            del self.open_trades_dict[trade.request.entry_request_id]
            
    def is_request_accepted(self, request):
        return True 
    
    
    def manage_entry_request(self, entry_request):
        """
        It decides wheather to trade or not and how much.
        It returns a Trade object or None.
        """
        if(self.is_request_accepted(entry_request)):
            trade = self.make_trade(entry_request)
            exit_strategy = StopLoss(strategy_id = "Exit coward: Str" + str(entry_request.strategy_id) + ":" + str(entry_request.entry_request_id), trade = trade, portfolio = self.portfolio)
            exit_strategy.set_velas(trade.request.symbol_name, self.portfolio[trade.request.symbol_name].timeframes_list[0])
            exit_strategy.set_stop_loss(pct = 0.1)
            self.coliseum.add_exit_strategy(exit_strategy)
            
            first_exit_request = self.coliseum.get_exit_strategy(exit_strategy.strategy_id).compute_first_exit_request()
            if first_exit_request is not None:
                self.coliseum.queue.put(first_exit_request)
        else:
            trade = None
        
        return trade
    
    def manage_exit_request(self, exit_request):
        """
        It decides wheather to trade or not and how much.
        It returns a Trade object or None.
        """
        if(self.is_request_accepted(exit_request)):
            trade = self.make_trade(exit_request)
            self.coliseum.del_exit_strategy(exit_request.strategy_id)
        else:
            trade = None
        
        return trade
    
    def backtest(self):
        # Compute all the entry requests of the trade.
        self.coliseum.compute_requests_queue()
        
        while self.coliseum.queue.empty() == False:
            request = self.coliseum.queue.get()[1]
            
            print(request)
            if isinstance(request, EntryRequest):
                self.manage_entry_request(request)
            elif isinstance(request, ExitRequest):
                self.manage_exit_request(request)
            
#            self.coliseum.compute_first_exit_requests()
            
            