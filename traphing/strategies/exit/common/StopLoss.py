import pandas as pd
import numpy as np
import datetime as dt

from .. import ExitStrategy, ExitSignal
from .... import utils as ul

class StopLoss(ExitStrategy):
    """ 
    Exit the trade if it has lost X percent of its value.
    """

    def __init__(self, strategy_id, entry_signal, portfolio = None, symbol_name = None, timeframe = None):
        super().__init__(strategy_id, portfolio)
        self.signal_names = ["slow_MA", "fast_MA"]
        
        self.symbol_name = symbol_name
        self.timeframe = timeframe
        self.stop_loss = None
        
    # Set the parameters of the trailing stop: Commodity, period and % 
    
    def set_stop_loss(self, price = None, pct = None):
        """
        It sets the value of the stop loss
        """
        if price is not None:
            self.stop_loss = price
        else:
            price = self.trade.trade_price
            sign = 1
            if self.trade.BUYSELL == "SELL":
                sign = -1
            self.stop_loss = price*(1 + sign*pct/100)
            
    def set_velas(self, symbol_name, timeframe):
        self.symbol_name = symbol_name
        self.timeframe = timeframe
    
    def compute_signals(self):
        close = self.porfolio[self.symbol_name][self.timeframe]["Close"]
        return close
    
    def check_exit(self):
        signals = self.compute_signals()
        
        if self.trade.BUYSELL == "SELL":
            idx_cross = np.where(signals > self.stop_loss)
        else:
            idx_cross = np.where(signals < self.stop_loss)
            
        series = pd.Series(np.zeros((signals.size)), index = signals.index, name = "Crosses")
        series[idx_cross] = 1
        
        return series

        
    def get_exit_signal(self):
        # Creates the EntryTradingSignals for Backtesting
        crosses,dates = self.get_TradeSignals()
        
        list_events = []
        # Buy signals
        Event_indx = np.where(crosses != 0 ) # We do not care about the second dimension
        for indx in Event_indx[0]:
            # Create the Exit signal !
            if crosses[Event_indx] == 1:
                BUYSELL = "BUY"
            else:
                BUYSELL = "SELL"
                
            entrySignal =  CExS.CExitSignal(StrategyID = self.StrategyID, 
                                            EntrySignalID = str(self.singalCounter), 
                                            datetime = dates[indx], 
                                            symbolID = self.slowMAparam["SymbolName"], 
                                            BUYSELL = BUYSELL)
            entrySignal.comments = "Basic Crossing MA man !"
            
            entrySignal.priority = 0
            entrySignal.recommendedPosition = 1 
            entrySignal.tradingStyle = "dayTrading"
            
            list_events.append(entrySignal)
            self.singalCounter += 1
        
        return list_events