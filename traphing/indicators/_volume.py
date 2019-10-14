import numpy as np
import pandas as pd  
from . import indicators_lib as indl

#Accumulation/Distribution  
def ACCDIST(df, n = 14):  
    MFM = (2 * df['Close'] - df['High'] - df['Low']) / (df['High'] - df['Low']) 
    MFV  =  MFM* df['Volume'] 
    # TODO: I dont get this
#    M = ad.diff(n - 1)  
#    N = ad.shift(n - 1)  
#    AD = M / N  
#    
#    AD = pd.ewma(AD, span = n, min_periods = n - 1)  
#    AD = pd.rolling_sum(AD, window = n)
    ADL = np.cumsum(np.nan_to_num(MFV))
    series = pd.Series(ADL, name = "ADL(%i)"%n)
    return series
    
