import pandas as pd
import numpy as np
from typing import Type
import datetime as dt
import sys

from ..data_classes import Portfolio
from ..strategies import Trade, Coliseum, TradeRequest, Strategy
from ..strategies.entry import EntryTradeRequest
from ..strategies.exit import ExitTradeRequest, StopLoss, ExitStrategy
from ..utils import BrainModes, unwrap

class Brain:
    """Main system class that handles everyhing
    """
    def __init__(self, coliseum: Coliseum, portfolio: Portfolio, 
                 mode: BrainModes = BrainModes.BACKTEST_BATCH):
        self.coliseum = coliseum
        self.money_management = None
        self.portfolio = portfolio

        self.trade_counter = 0
        
        self.open_trades_dict = dict()
        self.closed_trades_pairs_dict = dict()
        
        self.mode = mode

    """
    ###################### Managing requests methods #########################
    """
    def manage_entry_request(self, entry_request: EntryTradeRequest) -> Trade:
        """It handles the handling logic of an entry request.
        If the request is accepted and a trade is made, it returns a Trade object,
        otherwise it returns None.
        
        The logic is as follows:
            - If the request is accepted, an associated trade is made.
            - If the trade is sucessful, it creates its corresponding exit strategy
            object and adds the strategy to the coliseum. 
            - In BACKTEST_BATCH mode, it computes the first exit request of the strategy
            and puts it in the coliseums' queue.
        """
        
        if self.is_request_accepted(entry_request):
            trade = self.make_trade(entry_request)
            exit_strategy = self._get_associated_exit_strategy(trade)
            self.coliseum.add_exit_strategy(exit_strategy)
            
            if(self.mode == BrainModes.BACKTEST_BATCH):
                self._generate_exit_requests_for_backtesting(exit_strategy.name)
        else:
            trade = None
        
        return trade
    
    def manage_exit_request(self, exit_request: ExitTradeRequest) -> Trade:
        """It handles the handling logic of an entry request.
        If the request is accepted and a trade is made, it returns a Trade object,
        otherwise it returns None.
        
        The logic is as follows:
            - If the request is accepted, an associated trade is made.
            - If the trade is sucessful, the associated exit strategy is deleted.
        """
        
        if(self.is_request_accepted(exit_request)):
            trade = self.make_trade(exit_request)
            self.coliseum.del_exit_strategy(exit_request.strategy_name)
        else:
            trade = None
        
        return trade

    def is_request_accepted(self, request: Type[TradeRequest]) -> bool:
        """Returns true if the request is accepted and so a trade is going
        to take place.
        """
        if self.mode == BrainModes.BACKTEST_BATCH:
            return True
        return True 
    

    def make_trade(self, request: Type[TradeRequest]) -> Trade:
        """Makes the trade associated to a request.
        """
        trade = Trade(name = "trade_" + request.name, request = request,
             price = request.price)

        self._log_trade(trade)
        return trade

    """
    ###################### Managing trades methods #########################
    """
    
    def _log_trade(self, trade: Trade):
        """It logs the performed trade.
        If it is an entry trade: It includes it into the open_trades_dict
        If it is an exit trade: It includes the  [entry_trade, exit_trade] pair in
        the closed_trades_pairs_dict. It also removes the corresponding entry trade
        from open_trades_dict.
        """
        if isinstance(trade.request, EntryTradeRequest):
            self.open_trades_dict[trade.name] = trade
            
        elif isinstance(trade.request, ExitTradeRequest):
            self.closed_trades_pairs_dict[trade.request.entry_trade.name] = [self.open_trades_dict[trade.request.entry_trade.name], trade]
            del self.open_trades_dict[trade.request.entry_trade.name]
            

    def _get_associated_exit_strategy(self, trade: Trade) -> Type[ExitStrategy]:
        """Fetches the entry_strategy object related to an trade and
        creates the exit_strategy object from it using its method create_exit_strategy()
        """
        entry_strategy_name = trade.request.strategy_name
        entry_strategy = self.coliseum.get_entry_strategy(entry_strategy_name)
        exit_strategy = entry_strategy.create_exit_strategy(trade)
        return exit_strategy

    """
    ###################### Special backtesting methods #########################
    """
    
    def _generate_exit_requests_for_backtesting(self, exit_strategy_name: str):
        """Computes the first exit request of the given exit strategy and puts it 
        in the coliseums queue.
        """
        
        first_exit_request = self.coliseum.get_exit_strategy(exit_strategy_name).compute_first_exit_request()
        if first_exit_request is not None:
            self.coliseum.queue.put(first_exit_request)
                
    """
    ###################### Interface methods #########################
    """
    
    def backtest(self):
        """Performs the backtest in BACKTEST_BATCH mode.
        The analysis of the backtest will be computed from the dictionaries
        open_trades_dict and closed_trades_pairs_dict
        """
        self.coliseum.compute_requests_queue()
        
        print ("----- Performing Backtesting ---------")
        print ("Period: " + str(self.portfolio.start_time.date()) + " - " + str(self.portfolio.end_time.date()))
        print ("Total number of entry trade requests: ",self.coliseum.queue.qsize())
 
        n_request_handled = 0
        
        print("")
        while self.coliseum.queue.empty() == False:
            request = self.coliseum.queue.get()[1]
            n_request_handled += 1
            
            relative_time_done = (request.timestamp - self.portfolio.start_time).total_seconds()*100
            relative_time_done /= (self.portfolio.end_time - self.portfolio.start_time).total_seconds() +60*60*24
            text = "Req: %i: %s"%(n_request_handled, request.name) + \
            ". Time: " + str(request.timestamp.date()) + " pct time: %.2f%s"%(relative_time_done,"%")
#            
#            unwrap(request)
            print("\r" + "    "*40, end = "")
            print("\r" + text, end = "")
#            print(text)
            if isinstance(request, EntryTradeRequest):
                self.manage_entry_request(request)
            elif isinstance(request, ExitTradeRequest):
                self.manage_exit_request(request)
            
#            self.coliseum.compute_first_exit_requests()
            
            