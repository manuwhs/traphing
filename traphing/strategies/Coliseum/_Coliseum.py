from typing import List, Type
from queue import PriorityQueue
from .. import Strategy
from ...graph.Gl import gl

class Coliseum:
    """Class with functionalities to control all entry and exit strategies!
    It provides an interface between the brain and all the strategies.
    """
    def __init__(self):
        self._entry_strategies_dict = dict() 
        self._exit_strategies_dict = dict() 
        
        self.queue = PriorityQueue()
        
    def add_entry_strategy(self, strategy: Type[Strategy]):
        self._entry_strategies_dict[strategy.name] = strategy

    def add_exit_strategy(self, strategy: Type[Strategy]):
        self._exit_strategies_dict[strategy.name] = strategy

    def del_entry_strategy(self, name: str):
        del self._entry_strategies_dict[name]

    def del_exit_strategy(self, name: str):
        del self._exit_strategies_dict[name]
    
    def get_entry_strategy(self, name: str) -> Type[Strategy]:
        return self._entry_strategies_dict[name]

    def get_exit_strategy(self, name: str) -> Type[Strategy]:
        return self._exit_strategies_dict[name]
        
    @property
    def entry_strategies_names_list(self) -> List[str]:
        return list(self._entry_strategies_dict.keys())

    @entry_strategies_names_list.setter
    def entry_strategies_names_list(self, value:  List[str]):
        ValueError("This property cannot be set externally")

    @property
    def exit_strategies_names_list(self) -> List[str]:
        return list(self._exit_strategies_dict.keys())

    @exit_strategies_names_list.setter
    def exit_strategies_names_list(self, value:  List[str]):
        ValueError("This property cannot be set externally")
        
    """
    ############### Methods to handle all the queues ####################
    """
    
    def compute_entry_requests_queue(self):
        """Computes the queue of all entry strategies and puts its elements
        in the coliseum queue.
        """
        for entry_strategy_name in self.entry_strategies_names_list:
            entry_strategy = self.get_entry_strategy(entry_strategy_name)
            
            entry_strategy_queue = entry_strategy.compute_requests_queue()
            while entry_strategy_queue.empty() == False:
                self.queue.put(entry_strategy_queue.get())
        return self.queue
    
    def compute_exit_requests_queue(self):
        """Computes the queue of all exit strategies and puts its elements
        in the coliseum queue.
        """
        for exit_strategy_name in self.exit_strategies_names_list:
            exit_strategy = self._exit_strategies_dict[exit_strategy_name]
            
            exit_strategy_queue = exit_strategy.compute_requests_queue()
            while (exit_strategy_queue.empty() == False):
                self.queue.put(exit_strategy_queue.get())
        return self.queue
    
    def compute_requests_queue(self):
        """Computes the queue of all strategies and puts its elements
        in the coliseum queue.
        """
        self.compute_entry_requests_queue()
        self.compute_exit_requests_queue()
        return self.queue
    
    def compute_first_exit_requests(self):
        """It computes the first exit request of all exit strategies and puts it
        inside the coliseum queue. This function is used in backtesting for
        optimization purposes and to avoid puting exit requests in the coliseum 
        queue for trades that have already been closed.
        """
        for exit_strategy_id in self.exit_strategies_names_list:
            exit_strategy = self.get_exit_strategy(exit_strategy_id)
            queue = exit_strategy.compute_exit_requests_queue()
            if queue.empty() == False:
                element = queue.get()
                self.queue.put(element)
        return self.queue
    
    """
    ############### Extra methods for visualization ####################
    """
    def plot_strategies(self, axes_list = []):
        """
        Plotting function that makes it convenient to visualize the strategy.
        It computes everything so maybe dont use it for real time, just
        for exploratory analysis.
        
        The axes list should be 2 times the number of strategies
        """
        
        i = 0
        for strategy_id in self.entry_strategies_ids_list:
            ax1 = axes_list[i*2]; ax2 = axes_list[i*2+1]
            entry_strategy = self.get_entry_strategy(strategy_id)
            entry_strategy_series = entry_strategy.compute_strategy_series()
            entry_series = entry_strategy.compute_entry_series()
        
            ##TODO
            if(False):
                portfolio[symbol_name][timeframe].plot_barchart(axes = ax1, labels = ["", "", strategy_id])
            gl.plot(entry_strategy_series.index, entry_strategy_series, legend = list(entry_strategy_series.columns), axes =ax1)
        
            gl.stem(entry_strategy_series.index,entry_series, axes = ax2, legend = "Trades")
        
            i = i+1
            
            
        