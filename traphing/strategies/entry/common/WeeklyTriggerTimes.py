import numpy as np
import pandas as pd

from .. import EntryStrategy
from ...exit import StopLoss
from ... import Trade
from ....data_classes import Portfolio

class WeeklyTriggerTimes(EntryStrategy):
    """Strategy: It makes a BUY trade every at the given times in the given weekdays.
    Example of params:
        params = {"velas":{"symbol_name":"AUDCHF","timeframe": Timeframes.M15}, 
                  "weekly_trigger_times": 
                      {"weekdays_list":[0,2,4], 
                       "times_list":[dt.time(4,0,0),dt.time(12,0,0)]}}

    """
    def __init__(self, name: str, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, portfolio, params)
        self.input_series_names = ["velas","weekly_trigger_times"]
    
    def compute_input_series(self):
        symbol_name = self.params["velas"]["symbol_name"]
        timeframe = self.params["velas"]["timeframe"]
        weekdays_list = self.params["weekly_trigger_times"]["weekdays_list"]
        
        velas = self.portfolio[symbol_name][timeframe]
        
        weekday_triggers_list = []
        for weekday_number in weekdays_list:
            threshold = pd.Series(np.ones(velas.timestamps.size) * weekday_number, 
                                  index = velas.timestamps, name = "weekly_trigger_day%i"%weekday_number)
            weekday_triggers_list.append(threshold)
        
        
        weekdays_velas = pd.Series(velas.timestamps.map(pd.Timestamp.weekday).values,
                                   index = velas.timestamps, name = "velas")
        
        
        series_df = pd.concat([*weekday_triggers_list, weekdays_velas],axis = 1)
        return series_df
    
    def compute_trigger_series(self):
        series_df = self.compute_input_series()
        weekdays_list = self.params["weekly_trigger_times"]["weekdays_list"]
        time_list = self.params["weekly_trigger_times"]["times_list"]
        
        equal_day_indexes = [False]*series_df["velas"].index.size
        for weekday_number in weekdays_list:
            equal_day_indexes |= series_df["velas"] == series_df["weekly_trigger_day%i"%weekday_number]
        
        beginning_of_day_indexes = [False]*series_df["velas"].index.size
        
        for time in time_list:
            beginning_of_day_indexes |= series_df["velas"].index.map(pd.Timestamp.time) == time
            
        indexes = equal_day_indexes & beginning_of_day_indexes

        trigger_series = pd.Series(np.zeros(series_df.index.size), 
                                   index = series_df.index, name = "trigger_entry")
        
        trigger_series[indexes] = 1
        
        return trigger_series
        
    def compute_requests_queue(self):
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0)[0] # We do not care about the second dimension
        
        for indx in Event_indx:
            action = self._get_action(trigger_series[indx])
            timestamp = trigger_series.index[indx]
            symbol_name = self.params["velas"]["symbol_name"]
            timeframe = self.params["velas"]["timeframe"]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, price, action)

        return self.queue
    
    def create_exit_strategy(self, trade: Trade):
        exit_strategy = StopLoss(name = "StopLoss_for_" + trade.name, trade = trade, portfolio = self.portfolio)
        
        symbol_name = trade.request.symbol_name
        timeframe = self.portfolio[trade.request.symbol_name].timeframes_list[0]
        exit_strategy.params["velas"] = {"symbol_name":symbol_name, "timeframe":timeframe}
        exit_strategy.set_stop_loss(pct = 0.3)
        return exit_strategy
        
        