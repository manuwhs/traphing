import numpy as np
import pandas as pd  
from . import indicators_lib as indl

#Stochastic oscillator %K and %D  
def STO(df, n = 14, SK = 3, SD = 3):  
    SOk = STOK(df, n = n, SK = SK )
#    SOd = pd.ewma(SOk, span = n, min_periods = n - 1)
    SOd = STOD(df, n = n, SK = 3, SD = SD)
    return pd.concat([SOk,SOd], axis=1)

#Stochastic oscillator %K  
def STOK(df, n = 14, SK = 1):  
    # TODO: This could be inf
    SOk = np.zeros((df.shape[0],1))
    
    maxH = df['High'].rolling(window = n, min_periods = n-1).max()
    minL = df['Low'].rolling( window = n, min_periods = n-1).min()
    
    SOk = (df['Close'] - minL) / (maxH - minL)
#    SOk = SOk.fillna(1)
    
    # Instead of computing the min and max of each n-window,
    # we reuse the previous min and max :)
    if (SK > 1):
        SOk = SOk.ewm( span = SK, min_periods = SK - 1).mean()*100
    SOk.name = "SOk(%i,%i)"%(n,SK)
    return SOk

#Stochastic oscillator %D  
def STOD(df, n = 14, SK = 3, SD = 3):  
    SOk = STOK(df, n = n )
#    SOd = pd.ewma(SOk, span = n, min_periods = n - 1)
    SOd = SOk.rolling(window = SD, min_periods = SD - 1).mean()*100
    SOd.name = "SOd(%i,%i,%i)"%(n,SK,SD)
    return SOd

#MACD, MACD Signal and MACD difference  
def MACD(df, n_fast = 26, n_slow = 12, n_smooth = 9):  
    EMAfast = df['Close'].ewm( span = n_fast, min_periods = n_slow - 1).mean()
    EMAslow = df['Close'].ewm( span = n_slow, min_periods = n_slow - 1).mean()
    
    MACD = EMAfast - EMAslow
    MACDsign = MACD.ewm( span = 9, min_periods = 8).mean()
    MACDdiff = MACD - MACDsign

    dataframe = pd.concat([MACD,MACDsign,MACDdiff], axis=1, keys = ["MACD","MACDsign","MACDdiff"])
    return  dataframe

#Trix  
## Oscillator similar to MACD
def TRIX(df, n1 = 12, n2 = 12, n3 = 12):  
    EX1 = df['Close'].ewm( span = n1, min_periods = n1 - 1).mean()
    EX2 = EX1.ewm( span = n2, min_periods = n2 - 1).mean()
    EX3 = EX2.ewm( span = n3, min_periods = n3 - 1).mean()  
    # Get the returns 
    Trix = EX3.pct_change(periods = 1)
    dataframe = pd.concat([Trix, EX1,EX2,EX3], axis=1, keys = ["Trix","EX1","EX2","EX3"])
    return dataframe
    
#Relative Strength Index  
def RSI(df, n = 20):  

    deltas = df["Close"] - df["Open"]
    # For the first N samples we will not be able to do it properly

    ## What we do is a rolling mean of the positive and the negative
    dUp, dDown = deltas.copy(), deltas.copy()
    ## Vector of positive and negative
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0
    # print (dUp)
    # Calculate the rolling mean, the Window !!
    # Calculates the average dUp and dDown in time
    RolUp = np.array(dUp.rolling( n).mean().values).flatten()
    RolDown =np.array( dDown.rolling( n).mean().values).flatten()

    # Finally compute the shit
    RS = np.abs(RolUp / (RolDown +0.0000001)) # To avoid division by 0
    RSI = 100. - (100. / (1. + RS))

    dataframe = pd.DataFrame([RS,RSI]).T
    dataframe.index = df.index
    dataframe.columns = ["RS(%i)"%(n),"RSI(%i)"%(n)]
    return dataframe
    
#Average Directional Movement Index  
def ADX(df, n = 14, n_ADX = 14):  
    i = 0  
    UpI = []  
    DoI = []  
    while i + 1 < len(df.index):  
        UpMove = df.get_value(df.index[i + 1], 'High') - df.get_value(df.index[i], 'High')  
        DoMove = df.get_value(df.index[i], 'Low') - df.get_value(df.index[i + 1], 'Low')  
        if UpMove > DoMove and UpMove > 0:  
            UpD = UpMove  
        else: UpD = 0  
        UpI.append(UpD)  
        if DoMove > UpMove and DoMove > 0:  
            DoD = DoMove  
        else: DoD = 0  
        DoI.append(DoD)  
        i = i + 1  
    i = 0  
    TR_l = [0]  
    while i < len(df.index) -1:  
        TR = max(df.get_value(df.index[i + 1], 'High'), 
                 df.get_value(df.index[i], 'Close')) - min(df.get_value(df.index[i + 1], 'Low'), 
                df.get_value(df.index[i], 'Close'))  
        TR_l.append(TR)  
        i = i + 1  
    TR_s = pd.Series(TR_l)  
    ATR = pd.Series(pd.ewma(TR_s, span = n, min_periods = n))  
    UpI = pd.Series(UpI)  
    DoI = pd.Series(DoI)  
    PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1) / ATR)  
    NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1) / ATR)  
    ADX = pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span = n_ADX, min_periods = n_ADX - 1)  
    
    ADX = ul.fnp(ADX)
    return ADX
    
