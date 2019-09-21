"""
Moving averages library.
The inputs are pandas dataframe with OCHLV data
"""
import pandas as pd
import numpy as np

# The values is already a correct [Nsam, Nsig] numpy matrix
#Moving Average  
def SMA(df: pd.DataFrame, series_name: str = "Close", n: int = 20):  
    SMA = df[series_name].rolling(n).mean()
    return SMA

#Exponential Moving Average  
def EMA(df: pd.DataFrame, series_name: str = "Close", n: int = 20):  
    EMA = pd.Series.ewm(df[series_name], span = n,min_periods = n).mean()
    return EMA


def get_WMA(df: pd.DataFrame, series_name: str = "Close", n: int = 20):  

    return total_sM
    
def get_TrCrMr (time_series, alpha = -1):
    """ Triple Cruce de la Muerte. Busca que las exponenciales 4, 18 y 40 se crucen
    para ver una tendencia en el mercado despues de un tiempo lateral """
    L1 = 4
    L2 = 18
    L3 = 40
    
    eM1 = get_EMA(time_series, L1, alpha)
    eM2 = get_EMA(time_series, L2, alpha)
    eM3 = get_EMA(time_series, L3, alpha)
    return np.concatenate((eM1,eM2,eM3), axis = 1)

def get_HMA (time_series, L, cval = np.NaN):
    """ Hulls Moving Average !! L = 200 usually"""
    WMA1 = get_WMA(time_series, int(L/2), cval = cval) * 2
    WMA2 = get_WMA(time_series, int(L), cval = cval)
    
    HMA = get_WMA(WMA1 - WMA2, int(np.sqrt(L)), cval =cval)
    
    return HMA
    
def get_HMAg (time_series, L, alpha = -1,  cval = np.NaN):
    """ Generalized Moving Average from Hull"""
    ## Moving Average of 2 moving averages.
    ## It uses Exponential Moving averages
    EMA1 = get_EMA(time_series, L/2, alpha, cval = cval) * 2
    EMA2 = get_EMA(time_series, L, alpha, cval = cval)
    
    EMA = get_EMA(EMA1 - EMA2, np.sqrt(L), alpha, cval = cval)
    
    return EMA


def get_TMA(time_series, L):
    """ First it trains the data so that the prediction is maximized"""
    ### Training phase, we obtained the MSQE of the filter for predicting the next value
    time_series = time_series.flatten()
    Ns = time_series.size
    
    Xtrain, Ytrain = ul.windowSample(time_series, L)
    

    window = np.linalg.pinv((Xtrain.T).dot(Xtrain))
    window = window.dot(Xtrain.T).dot(Ytrain)
    window = np.fliplr([window])[0]
    gl.stem([],  window)

    sM = np.convolve(time_series.flatten(),window.flatten(), mode = "full")
    
#    print sM.shape
    sM = sM
    sM = sM/np.sum(window)    # Divide so that it is the actual mean.
    
    sM[:L] = (np.ones((L,1)) * sM[L]).flatten()  # Set the first ones equal to the first fully obtained stimator
    sM = sM[:-L+1]    # Remove the last values since they hare convolved with 0's as well
    return sM
