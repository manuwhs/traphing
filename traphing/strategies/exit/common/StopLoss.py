import pandas as pd
import numpy as np
import datetime as dt

from .. import ExitStrategy, ExitRequest
from .... import utils as ul

class StopLoss(ExitStrategy):
    """ 
    Exit the trade if it has lost X percent of its value.
    """

    def __init__(self, strategy_id, trade, portfolio = None, symbol_name = None, timeframe = None):
        super().__init__(strategy_id, trade, portfolio)
        self.series_names = ["Close","Stop_loss"]
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
            if self.trade.BUYSELL == "SELL":
                sign = 1
            elif self.trade.BUYSELL == "BUY":
                sign = -1
            self.stop_loss = price*(1 + sign*pct/100)
        
    def set_velas(self, symbol_name, timeframe):
        self.symbol_name = symbol_name
        self.timeframe = timeframe
    
    def compute_strategy_series(self):
        close = self.portfolio[self.symbol_name][self.timeframe].series("Close")
        stop_loss = pd.Series(np.ones(close.index.size) * self.stop_loss, index = close.index)
        series = pd.concat([close,stop_loss],axis =1, keys = self.series_names)
        
        # Set to none the samples before the event
        series[series.index < self.trade.request.candlestick_timestamp] = np.NaN
        return series
    
    def compute_exit_series(self):
        signals = self.compute_strategy_series()
        series = ul.check_crossing(signals["Stop_loss"],signals["Close"])
        series = series.abs()
        return series

        
    def compute_exit_requests_queue(self):
        # Creates the EntryTradingSignals for Backtesting
        crosses = self.compute_exit_series()
        Event_indx = np.where(crosses != 0 )[0] # We do not care about the second dimension
        for indx in Event_indx:
            candlestick_timestamp = crosses.index[indx]
            symbol_name = self.symbol_name; timeframe = self.timeframe
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(candlestick_timestamp)["Close"])
            
            exit_request =  ExitRequest(exit_request_id = str(self.exit_requests_counter), 
                                       strategy_id = self.strategy_id, 
                                       candlestick_timestamp = candlestick_timestamp,
                                       BUYSELL = self.trade.BUYSELL, price = price, symbol_name = symbol_name)
            
            exit_request.comments = "Getting out of MA!"
            exit_request.priority = 0
            exit_request.recommendedPosition = 1 
            exit_request.tradingStyle = "dayTrading"
            
            self.queue.put((crosses.index[indx], exit_request))
            self.exit_requests_counter += 1
        
        return self.queue
