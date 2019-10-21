
import datetime as dt
from ..graph.Gl import gl
from ..strategies import Trade
from ..strategies.exit import ExitTradeRequest

class ClosedTradeAnalysis:
    """
    Class that contains all the info of a closed trade and performs the operations
    to analyze it.
    """
    def __init__(self, entry_trade, exit_trade):
        
        self.faked_exit_trade = False
        
        self.entry_trade = entry_trade
        self.exit_trade = exit_trade
        
        self.entry_price = None
        self.gain = None
        self.duration = None
        
        self.buy_sell_factor = None
        self.compute_basics()
    
    @classmethod
    def from_open_trade(cls, entry_trade, portfolio):
        """
        This function fakes a closed trade.
        """
        
        # Create fake Exit trade request with current data
        name =  "End of backtest fake exit for " + entry_trade.name
        trade = entry_trade
        action = entry_trade.request.action
        
        symbol_name = entry_trade.request.symbol_name
        last_candlestick = portfolio[symbol_name].get_closest_past_candlestick(dt.datetime.now())
        timestamp = last_candlestick.index[0]

        price = float(last_candlestick["Close"])
        
        fake_exit_request = ExitTradeRequest(name, trade, timestamp, symbol_name, price, action)
        
        # Create fake Exit trade
        fake_exit_trade = Trade(name = "trade_" + fake_exit_request.name, request = fake_exit_request,
             price = fake_exit_request.price)
        
        obj = cls(entry_trade, fake_exit_trade)
        obj.faked_exit_trade = True
        return obj
    
    def compute_basics(self):
        self.entry_price = self.entry_trade.price
        self.exit_price = self.exit_trade.price

#        self.entry_timestamp = self.entry_trade.trade_timestamp
#        self.exit_timestamp = self.exit_trade.trade_timestamp

        self.entry_timestamp = self.entry_trade.request.timestamp
        self.exit_timestamp = self.exit_trade.request.timestamp
        
        self.buy_sell_factor = self.entry_trade.request.action.value
        
        self.gain = (self.exit_price - self.entry_price)*self.buy_sell_factor
        
        self.duration = self.exit_timestamp - self.entry_timestamp
    
    def print_summary(self):
        print("-> Trade: ",self.entry_trade.request.name," - ",self.exit_trade.request.name)
        print("entry_timestamp", self.entry_timestamp , ". entry_price: ",self.entry_price)
        print("gain: ",self.gain/self.entry_price*100, "%")
        print("duration: ", self.duration)
        
    def plot_trade_line(self, axes = None):
        """
        It plots from origin to end a line
        """
        ls = "-"
        if(self.faked_exit_trade):
            ls = "--"
        gl.plot([self.entry_timestamp, self.exit_timestamp],[self.entry_price, self.exit_price], axes = axes,
                legend = ["Gain: %.2f "%(self.gain/self.entry_price*100)], ls = ls)

class BacktestAnalysis:
    """
    Class that automatizes a given analysis
    """
    def __init__(self, brain):
        self.brain = brain
    
    def backtest(self):
        self.brain.backtest()

    def get_trade_analysis(self):
        trade_analysis_list = []
        for closed_trade_name in list(self.brain.closed_trades_pairs_dict.keys()):
            entry_trade, exit_trade = self.brain.closed_trades_pairs_dict[closed_trade_name]
            trade_analysis = ClosedTradeAnalysis(entry_trade,exit_trade)
            trade_analysis_list.append(trade_analysis)

        for open_trade_name in list(self.brain.open_trades_dict.keys()):
            entry_trade = self.brain.open_trades_dict[open_trade_name]
            trade_analysis = ClosedTradeAnalysis.from_open_trade(entry_trade,self.brain.portfolio)
            trade_analysis_list.append(trade_analysis)
        return trade_analysis_list
    
    """
    ############ Methods over all the trades ################
    """
    def print_gains(self):
        trade_analysis_list = self.get_trade_analysis()
        for trade_analysis in trade_analysis_list:
            trade_analysis.print_summary()
    
    def plot_trades(self, axes = None):
        trade_analysis_list = self.get_trade_analysis()
        for trade_analysis in trade_analysis_list:
            trade_analysis.plot_trade_line(axes)
    
    def print_summary(self):
        trade_analysis_list = self.get_trade_analysis()
        gains_list = [trade_analysis.gain for trade_analysis in trade_analysis_list]
        duration_list = [trade_analysis.duration.total_seconds() for trade_analysis in trade_analysis_list]
        gl.init_figure()
        gl.scatter(duration_list, gains_list)