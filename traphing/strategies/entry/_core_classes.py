import pandas as pd
from typing import Type

from .. import exit as exit_strategies_module
from .. import TradeRequest, Strategy
from ..exit import ExitStrategy
from ...utils import Actions, Timeframes
from ...data_classes import Portfolio
from ... import utils as ul

class EntryTradeRequest(TradeRequest):
    """Contains the trade request information from an entry strategy.
    """
    def __init__(self, name, timestamp, symbol_name, timeframe, action, price):
        super().__init__(name, timestamp, symbol_name, timeframe, action, price)
        
class EntryStrategy(Strategy):
    """Parent class to be inherited by all entry strategies. 
    The ultimate goal of this class is to generate entry trate requests and 
    place them in its internal priority queue.
    """
    
    def __init__(self, name: str, portfolio: Portfolio = None,  params: dict = {}):
        super().__init__(name,portfolio, params)     
        self._set_exit_strategy_template()
    
    def set_params(self, params):
        super().set_params(params)
        self._set_exit_strategy_template()
        
    def _get_action(self, trigger_value: int):
        if (trigger_value == 1):
            action = Actions.BUY
        else:
            action = Actions.SELL
        return action
    
    def _set_exit_strategy_template(self):
        """Sets the parameters of the exit strategy associated to the trade.
        When a trade with this entry strategy is made, a corresponding exit strategy
        object will be created to handle it.
        """
        params = self.params
        try: 
            class_name = params["exit_strategy"]["class_name"]
            exit_params = params["exit_strategy"]["params"]
        except:
#            Warning("No exit strategy fields in the params dictionary. Setting default")
            class_name = "StopLoss"
            exit_params = {"portfolio": ul.get_empty_portfolio_params(),
                           "indicators": {"stop_loss_pct": 0.1}}
        
            self.params["exit_strategy"] = exit_params
            
        self.ExitStrategy = getattr(exit_strategies_module, class_name)
        self.exit_strategy_params = exit_params

    def create_request(self, timestamp: pd.Timestamp, symbol_name: str, timeframe: Timeframes,
                       price: float, action: Actions):
        """Creates an EntryTradeRequest object and puts it in its queue.
        """
        name =  self._generate_new_request_name()
        request =  EntryTradeRequest(name, timestamp, symbol_name, timeframe, price, action)
        self.queue.put((request.timestamp, request))

    def create_exit_strategy(self, trade: TradeRequest) -> Type[ExitStrategy]:
        """Creates a trading strategy from an entry trade
        If no specific strategy, return None.
        If the strategy needs extra information from the specific trade, it should
        find it within the trade object.
        """
        exit_strategy = self.ExitStrategy(name = "Exit_for_" + trade.name, 
                            trade = trade, portfolio = self.portfolio, 
                            params = self.exit_strategy_params)
        return exit_strategy
