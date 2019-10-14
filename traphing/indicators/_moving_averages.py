import pandas as pd  
from . import indicators_lib as indl

# Simple Moving Average 
def SMA(df, n = 20, series_name = "Close"):  
    values = df[series_name].rolling(n).mean()
    series = pd.Series(values, name = "SMA(%i)"%n)
    return series

#Exponential Moving Average  
def EMA(df, n = 20, series_name = "Close"):  
    values = pd.Series.ewm(df[series_name], span = n,min_periods = n).mean()
    series = pd.Series(values, name = "EMA(%i)"%n)
    return series
    
# Weighted Moving Average  
def WMA(df, n = 20, series_name = "Close"):  
    values = indl.WMA(df[series_name], n = n).flatten()
    series = pd.Series(values, name = "WMA(%i)"%n, index = df.index)
    return series

# Hull's Moving Average  
def HMA(df, n = 20, series_name = "Close"):  
    values = indl.HMA(df[series_name], n = n).flatten()
    series = pd.Series(values, name = "HMA(%i)"%n, index = df.index)
    return series

# Hull's Moving Average general
def HMAg(df, n = 20, series_name = "Close"):  
    values = indl.HMAg(df[series_name], n = n).flatten()
    series = pd.Series(values, name = "HMAg(%i)"%n, index = df.index)
    return series
