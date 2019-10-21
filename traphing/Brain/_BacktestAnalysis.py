
import datetime as dt
class BacktestAnalysis:
    """
    Class that automatizes a given analysis
    """
    def __init__(self, brain):
        self.brain = brain
    
    def backtest(self):
        self.brain.backtest()
        
    @classmethod
    def get_closed_trade_gain(cls, entry_trade, exit_trade):
        price_diff = exit_trade.trade_price - entry_trade.trade_price
        if (entry_trade.BUYSELL == "SELL"):
            price_diff*= -1
        return price_diff
    
    @classmethod
    def get_open_trade_gain(cls, entry_trade, price):
        price_diff = price - entry_trade.trade_price
        if (entry_trade.BUYSELL == "SELL"):
            price_diff*= -1
        return price_diff
    
    def print_gains(self):
        brain = self.brain
        for closed_trade_pair_id in list(brain.closed_trades_pairs_dict.keys()):
            entry_trade = brain.closed_trades_pairs_dict[closed_trade_pair_id][0]
            exit_trade = brain.closed_trades_pairs_dict[closed_trade_pair_id][1]
            print (BacktestAnalysis.get_closed_trade_gain(entry_trade,exit_trade))
        
        for entry_trade_id in list(brain.open_trades_dict.keys()):
            entry_trade = brain.open_trades_dict[entry_trade_id]
            price = brain.portfolio[entry_trade.request.symbol_name].get_closest_past_candlestick(dt.datetime.now())["Close"]
            
            print (BacktestAnalysis.get_open_trade_gain(entry_trade,price))
            
    