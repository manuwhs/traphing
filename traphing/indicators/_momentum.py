import numpy as np
import pandas as pd  
from . import indicators_lib as indl

# Return 
def RETURN(df, n = 1, series_name = "Close"):
    series = df[series_name]
    values = (series - series.shift(n))/series.shift(n)
    series = pd.Series(values, name = "RETURN(%i)"%n)
    return series

#Momentum  
def MOM(df, n = 1, series_name = "Close"):  
    MOM = df[series_name].diff(n) 
    MOM.name = "MOM(%i)"%(n)
    return MOM

#Rate of Change  
def ROC(df, n = 1, series_name = "Close"):  
    M = df[series_name].diff(n)
    N = df[series_name].shift(n)
#    print M.shape, N.shape
    ROC = M / N
    ROC.name = "ROC(%i)"%(n)
    return ROC