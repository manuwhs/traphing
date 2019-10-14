import pandas as pd  
import numpy as np
from . import indicators_lib as indl

#Standard Deviation  
def STD(df, n = 20, series_name = "Close"):  
    values = df[series_name].rolling(n, min_periods = n).std()
    series = pd.Series(values, name = "STD(%i)"%n)
    return series

# Average High - Low range
def AHLR(df, n = 14):  
    HLRange = df['High'] - df['Low']
#    AHLR_s = pd.ewma(HLRange, span = n, min_periods = n)
    values = HLRange.rolling(n).mean()
    series = pd.Series(values, name = "AHLR(%i)"%n)
    return series
    
#Average True Range  
def ATR(df, n = 14):  
    i = 0  
    TR_l = [np.NaN]  
    while i < len(df.index) -1:  
        CHCL = df.get_value(df.index[i + 1], 'High') - df.get_value(df.index[i + 1], 'Low')
        CLPC = df.get_value(df.index[i + 1], 'Low') -  df.get_value(df.index[i], 'Close')
        CHPC = df.get_value(df.index[i + 1], 'High') -  df.get_value(df.index[i], 'Close')
       
        TR = np.max(np.abs([CHCL,CLPC,CHPC]))
        TR_l.append(TR)  
        i = i + 1  
    
    values = pd.Series(TR_l).rolling( n).mean()
    series = pd.Series(values, name = "ATR(%i)"%n)
    return series
    
# Volatility Chaikin
def Chaikin_vol(df, n = 14):  
    HLRange = df['High'] - df['Low']
    EMA = HLRange.ewm( span = n, min_periods = n).mean()
    values = (EMA - EMA.shift(1))/EMA.shift(1)
    series = pd.Series(values, name = "Chaikin_vol(%i)"%n)
    return series
    