import datetime as dt
from ..graph.Gl import gl
from ..strategies import Trade
from ..strategies.exit import ExitTradeRequest
from ..strategies.entry import EntryTradeRequest
from ..data_classes import Portfolio

class ClosedTradeAnalysis:
    """
    Class that contains all the info of a closed trade and performs the operations
    to analyze it.
    """
    def __init__(self, entry_trade: EntryTradeRequest, exit_trade: ExitTradeRequest):
        
        self.entry_trade = entry_trade
        self.exit_trade = exit_trade
    
        self.faked_exit_trade = False
        self.compute_basics()
    
    @classmethod
    def from_open_trade(cls, entry_trade: EntryTradeRequest, portfolio: Portfolio):
        """Creates an object from the class faking a closed trade at the end 
        of the time interval.
        """
        # Create fake Exit trade request with current data
        name =  "End of backtest fake exit for " + entry_trade.name
        trade = entry_trade
        action = entry_trade.request.action
        
        symbol_name = entry_trade.request.symbol_name
        last_candlestick = portfolio[symbol_name].get_candlestick(dt.datetime.now())
        timestamp = last_candlestick.index[0]
        price = float(last_candlestick["Close"])
        
        fake_exit_request = ExitTradeRequest(name, trade, timestamp, symbol_name, price, action)

        # Create fake Exit trade
        fake_exit_trade = Trade("trade_" + fake_exit_request.name, 
                                fake_exit_request, fake_exit_request.price)
        
        obj = cls(entry_trade, fake_exit_trade)
        obj.faked_exit_trade = True
        return obj
    
    def compute_basics(self):
        """It computes the basic information of the trade from the entry_trade
        and exit_trade objects
        """
        
        self.entry_name = self.entry_trade.name
        self.exit_name = self.exit_trade.name
        
        self.entry_price = self.entry_trade.price
        self.exit_price = self.exit_trade.price
        
        self.symbol_name = self.entry_trade.request.symbol_name
        self.action = self.entry_trade.request.action
        self.buy_sell_factor = self.entry_trade.request.action.value
        
        self.entry_timestamp = self.entry_trade.request.timestamp
        self.exit_timestamp = self.exit_trade.request.timestamp
             
        self.gain = (self.exit_price - self.entry_price)*self.buy_sell_factor
        self.ret = self.gain/self.entry_price * 100
        self.duration = self.exit_timestamp - self.entry_timestamp
    
    
    def print_summary(self):
        """Prints a very basic summary of the trade. 
        """
        print("-> Trade: ",self.entry_trade.request.name," - ",self.exit_trade.request.name)
        print("entry_timestamp", self.entry_timestamp , ". entry_price: ",self.entry_price)
        print("gain: ",self.gain/self.entry_price*100, "%")
        print("duration: ", self.duration)
        
        
    def plot_trade_line(self, axes = None):
        """It plots a line from entry_trade [time,price] to the exit_trade [time,price]
        """
        ls = "-"
        if(self.faked_exit_trade):
            ls = "--"
            
        if self.gain >= 0:
            color = "b"
        else:
            color = "r"
        legend = ["Gain: %.2f "%(self.gain/self.entry_price*100)]
        
        gl.plot([self.entry_timestamp, self.exit_timestamp],[self.entry_price, self.exit_price], axes = axes,
                legend = [], ls = ls, lw = 1, alpha = 0.5, color = color)
        