import copy
import pandas as pd

from typing import List
from queue import PriorityQueue

class Coliseum:
    """
    Class with functionalities to control all entry and exit strategies!
    It provides an interface between the brain and all the strategies.
    """
    def __init__(self):
        self._entry_strategies_dict = dict() 
        self._exit_strategies_dict = dict() 
        
        self.queue = PriorityQueue()
        
    def add_entry_strategy(self, strategy):
        self._entry_strategies_dict[strategy.strategy_id] = strategy

    def add_exit_strategy(self, strategy):
        self._exit_strategies_dict[strategy.strategy_id] = strategy

    def del_entry_strategy(self, strategy_id):
        del self._entry_strategies_dict[strategy_id]

    def del_exit_strategy(self, strategy_id):
        del self._exit_strategies_dict[strategy_id]
    
    def get_entry_strategy(self, strategy_id):
        return self._entry_strategies_dict[strategy_id]

    def get_exit_strategy(self, strategy_id):
        return self._exit_strategies_dict[strategy_id]
        
    @property
    def entry_strategies_ids_list(self):
        return list(self._entry_strategies_dict.keys())

    @entry_strategies_ids_list.setter
    def entry_strategies_ids_list(self, value:  List[str]):
        ValueError("This property cannot be set externally")

    @property
    def exit_strategies_ids_list(self):
        return list(self._exit_strategies_dict.keys())

    @exit_strategies_ids_list.setter
    def exit_strategies_ids_list(self, value:  List[str]):
        ValueError("This property cannot be set externally")
        
    
    def compute_first_exit_requests(self):
        """
        It returns a queue with only the first exit request of the exit strategies
        """
        for exit_strategy_id in self.exit_strategies_ids_list:
            exit_strategy = self._exit_strategies_dict[exit_strategy_id]
            queue = exit_strategy.compute_exit_requests_queue()
            if(queue.empty() == False):
                element = queue.get()
                if (element not in self.queue.queue):
                    self.queue.put(element)
        return self.queue
    
    def compute_requests_queue(self):
        """
        Computes all of the strategies requests and joins them into a dictionary
        by date.
        """
        for entry_strategy_id in self.entry_strategies_ids_list:
            entry_strategy = self._entry_strategies_dict[entry_strategy_id]
            queue = entry_strategy.compute_entry_requests_queue()
            while (queue.empty() == False):
                self.queue.put(queue.get())
                
        for exit_strategy_id in self.exit_strategies_ids_list:
            exit_strategy = self._exit_strategies_dict[exit_strategy_id]
            queue = exit_strategy.compute_exit_requests_queue()
            while (queue.empty() == False):
                self.queue.put(queue.get())
        return self.queue
    
    def process_queue(self):
        while not self.requests_queue.empty():
            pass
