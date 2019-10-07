# -*- coding: utf-8 -*-

#### IMPORT the methods
import pandas as pd

from . import _core_functions as cf
from . import _database_functions as dbf
from . import _indicators as ind
from . import _plotting as pl

from ... import utils
from ...utils import Timeframes
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

class Velas:
    
    def __init__(self, symbol_name: str, timeframe: Timeframes):
        self.symbol_name = symbol_name    # Symbol of the Security (GLD, AAPL, IDX...)
        self.timeframe = timeframe        # It is the number of minutes of the period: 1 5 15....
        
        ## Time constraining variables
        self.start_time = None  # Start and end of period to operate from the TD
        self.end_time = None
        self._time_mask = None
        
        ## Related to the dataFrame with the data
        self._df = utils.get_empty_df()
        
        ## State variables
        self._trimmed = False

    
    ## Pandas dataframe with the dates.
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
    series = cf.series
    """
    Data loading functions
    """
    get_csv_file_path = dbf.get_csv_file_path    # Set and add timeData from csv's
    save_to_csv = dbf.save_to_csv
    load_data_from_csv = dbf.load_data_from_csv # Save timeData to csv
    add_data_from_csv = dbf.add_data_from_csv
    update_csv = dbf.update_csv

    """
    Indicators
    """
    # Moving Averages
    SMA = ind.SMA
    EMA = ind.EMA
    
    """
    Plotting
    """
    plot_barchart = pl.plot_barchart
    plot_series = pl.plot_series
    plot_candlesticks = pl.plot_candlesticks
    
if(0):


    get_SMA = TDind.get_SMA
    get_WMA = TDind.get_WMA
    get_EMA = TDind.get_EMA
    get_TrCrMr = TDind.get_TrCrMr
    get_HMA = TDind.get_HMA
    get_HMAg = TDind.get_HMAg
    get_TMA = TDind.get_TMA
    ############## Ocillators  ###########################################
    get_MACD = TDind.get_MACD
    get_momentum = TDind.get_momentum
    get_RSI = TDind.get_RSI
    ############## Volatility  ###########################################
    get_BollingerBand = TDind.get_BollingerBand
    get_ATR = TDind.get_ATR

    #######################################################################
    ############## Indicators from pandas  ###########################################
    #######################################################################

    # Moving Averages
    SMA = TDindp.SMA
    EMA = TDindp.EMA
    # Volatility
    STD = TDindp.STD
    AHLR = TDindp.AHLR
    ATR = TDindp.ATR
    Chaikin_vol = TDindp.Chaikin_vol
    # Price Channels
    PPSR  = TDindp.PPSR
    FibboSR = TDindp.FibboSR
    BBANDS = TDindp.BBANDS
    PSAR = TDindp.PSAR
    # Basic momentums
    MOM  = TDindp.MOM
    ROC = TDindp.ROC
    # Oscillators
    STO = TDindp.STO
    STOK = TDindp.STOK
    STOK = TDindp.STOK
    
    RSI = TDindp.RSI
    MACD = TDindp.MACD
    TRIX = TDindp.TRIX
    
    ADX = TDindp.ADX
    # Volume indicators
    ACCDIST = TDindp.ACCDIST

    #######################################################################
    ############## Graphics  ###########################################
    #######################################################################

    plot_timeSeries = TDgr.plot_timeSeries
    plot_timeSeriesReturn = TDgr.plot_timeSeriesReturn
    plot_timeSeriesCumReturn = TDgr.plot_timeSeriesCumReturn

    scatter_deltaDailyMagic = TDgr.scatter_deltaDailyMagic
    plot_TrCrMr = TDgr.plot_TrCrMr
    
    plot_BollingerBands = TDgr.plot_BollingerBands
#pd.concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False,
#       keys=None, levels=None, names=None, verify_integrity=False)
       