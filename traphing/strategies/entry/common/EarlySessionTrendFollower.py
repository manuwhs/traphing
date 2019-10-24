import numpy as np
import pandas as pd
import datetime as dt

from .. import EntryStrategy
from ....data_classes import Portfolio
from .... import utils as ul

class EarlySessionTrendFollower(EntryStrategy):
    """ This strategy performs a trade in a given time every day. The trade is BUY if the there has been an increase
    in price from the beggining of the session and SELL otherwise.
    
    
    Example of params:
        indicators = {"time":dt.time(2)}
    """
    def __init__(self, name: str, portfolio: Portfolio = None, params: dict = {}):
        super().__init__(name, portfolio, params)
    
    def compute_input_series(self) -> pd.DataFrame:
        symbol_name = self.symbol_names_list[0]
        timeframe = self.timeframes_list[0]
    
        symbol = self.portfolio[symbol_name]
        velas = self.portfolio[symbol_name][timeframe]
        
        dates_to_trading_session_dict = symbol.market_hours.get_timestamps_by_trading_session_dict(velas.timestamps)
        
        series_df = pd.Series(np.zeros(velas.timestamps.size),index = velas.timestamps, name = "gain")
        
        for date in list(dates_to_trading_session_dict.keys()):
            timestamps_date = dates_to_trading_session_dict[date]
            candlesticks_date = velas.df.loc[timestamps_date] # candlesticks of the date
            
            entry_time = self.params["indicators"]["time"]
            # We substract the timeframe because the timestamp time is the beggining of the candlestick
            timestamp_trigger = candlesticks_date.iloc[0].name + ul.to_timedelta(entry_time) - \
            dt.timedelta(minutes = velas.timeframe.value)
            
            open_trading_session_price = candlesticks_date.iloc[0]["Open"]
            first_hour_trading_session_close_price = candlesticks_date.loc[timestamp_trigger]["Close"]

            gain_first_hour = (first_hour_trading_session_close_price - open_trading_session_price)/first_hour_trading_session_close_price
            
            series_df.loc[timestamp_trigger] = gain_first_hour
            
        series_df = pd.concat([velas.series("Close"), series_df],axis = 1)
        return series_df
    
    def compute_trigger_series(self) -> pd.DataFrame:
        series_df = self.compute_input_series()
        trigger_series = series_df["gain"]
        trigger_series[trigger_series > 0] = 1
        trigger_series[trigger_series < 0] = -1
        pd.DataFrame(trigger_series, columns = [self.symbol_names_list[0]])
        return trigger_series
        
    def compute_requests_queue(self) -> pd.DataFrame:
        trigger_series = self.compute_trigger_series()
        Event_indx = np.where(trigger_series != 0)[0] # We do not care about the second dimension

        for indx in Event_indx:
            action = self._get_action(trigger_series[indx])
            timestamp = trigger_series.index[indx]
            symbol_name = self.symbol_names_list[0]
            timeframe = self.timeframes_list[0]
            price = float(self.portfolio[symbol_name][timeframe].get_candlestick(timestamp)["Close"])
            
            self.create_request(timestamp, symbol_name, timeframe, action, price)
        return self.queue
    