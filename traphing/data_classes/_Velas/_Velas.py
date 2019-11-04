import pandas as pd
from . import _core_functions as cf
from . import _database_functions as dbf
from . import _plotting as pl

from ... import utils
from ...utils import Timeframes

class Velas:
    """ A container to store prices for a symbol:
    This Class will contain for a given symbol:
      - Daily Data.
      - Intraday Data.
      
    Functions to:
    - Load data into it from any specific source 
    - Store itself into Disk to be loaded afterwards
    - """
    
    """ Dayly data will be a pandas Dataframe with the structure:
    
                  Open    High     Low   Close    Volume
    Date                                               
    2015-02-03  121.74  121.76  120.56  121.05   8255863
    2015-02-04  121.63  122.22  120.92  121.58   5386747
    2015-02-05  120.98  121.83  120.61  121.79   6879945
    2015-02-06  119.15  119.52  117.95  118.64  13206906
    
    Where Date is the index and is in dt.datetime.
    A set of functions for dealing with it will be specified. 
    Set of functions such as add values, delete values will be done.
    
    This class is intended for:
        - Load and save the Candlestick data.
        - Compute indicators based on Candlestick data
        - Deal with time 
        - Make some plottings
        
    Other operations such as returns should be computed externally. 
    Only the operation requiring indicators and combinations of OHLCV are 
    included in this library.
    """
    def __init__(self, symbol_name: str, timeframe: Timeframes):
        self.symbol_name = symbol_name    # Symbol of the Security (GLD, AAPL, IDX...)
        self.timeframe = timeframe        # It is the number of minutes of the period: 1 5 15....
        
        ## Time constraining variables
        self.start_time = None
        self.end_time = None
        self._time_mask = None
        
        ## Related to the dataFrame with the data
        self._df = utils.get_empty_df()
        
        ## State variables
        self._trimmed = False

    @property
    def df(self):
        if (self._time_mask is None):
            return self._df
        else:
            return self._df.iloc[self._time_mask]

    @df.setter
    def df(self, value: pd.DataFrame):
        if value is None:
            value = utils.get_empty_df()
        elif(utils.is_velas_df(value) == False):
            print (value)
            raise Warning("Setting a df dataframe with incorrect format")
            
        self._df = value
        ## Extra operations to perform
        self._df.sort_index(inplace=True)
        self.set_time_interval(trim = False)  # Set the interval to the maximum possible
        
    @property
    def timestamps(self):
        if (self._time_mask is None):
            return self._df.index
        else:
            return self._df.index[self._time_mask]

    @timestamps.setter
    def timestamps(self, value: pd.DatetimeIndex ):
        ValueError("Timestamps cannot be set externally")

    @property
    def dates(self):
        return self.timestamps.map(pd.Timestamp.date)

    @dates.setter
    def dates(self, value: pd.DatetimeIndex ):
        ValueError("Dates cannot be set externally")
        
    def __getitem__(self, key):
        val = self.series(key)
        return val
    
    """
    Core function methods
    """
    _get_time_mask = cf._get_time_mask
    set_time_interval = cf.set_time_interval
    
    is_trimmed = cf.is_trimmed
    add_df = cf.add_df
    _trim_df = cf._trim_df
    get_candlestick = cf.get_candlestick
    get_closest_past_candlestick = cf.get_closest_past_candlestick
    
    series = cf.series
    indicator = cf.indicator
    """
    Data loading functions
    """
    get_relative_csv_file_path = dbf.get_relative_csv_file_path    # Set and add timeData from csv's
    save_to_csv = dbf.save_to_csv
    load_data_from_csv = dbf.load_data_from_csv # Save timeData to csv
    add_data_from_csv = dbf.add_data_from_csv
    update_csv = dbf.update_csv
    
    """
    Plotting
    """
    plot_series = pl.plot_series
    plot_indicator = pl.plot_indicator
    plot_barchart = pl.plot_barchart
    plot_candlesticks = pl.plot_candlesticks
    
