import numpy as np
import pandas as pd  
from . import indicators_lib as indl

#Bollinger Bands  
def BBANDS(df, n = 20,  k = 2, series_name = "Close"):
    MA = df[series_name].rolling(n, min_periods = n ).mean()
    MSD =df[series_name].rolling(n, min_periods = n).std()

    BBh = MA + MSD *2
    BBl = MA - MSD *2
    
    ## Different types of BB bands ? TODO
#    b1 = 4 * MSD / MA  
#    b2 = (df[seriesNames] - MA + 2 * MSD) / (4 * MSD)  

    dataframe = pd.DataFrame([BBh,BBl]).T
    dataframe.index = df.index
    dataframe.columns = ["BBh(%i)"%(n),"BBl(%i)"%(n)]
    return dataframe

#Pivot Points, Supports and Resistances  
def PPSR(df):  
    PP = (df['High'] + df['Low'] + df['Close']) / 3
    
    R1 = 2 * PP - df['Low']
    S1 = 2 * PP - df['High']
    
    R2 = PP + df['High'] - df['Low']
    S2 = PP - df['High'] + df['Low']

#    R3 = df['High'] + 2 * (PP - df['Low'])  
#    S3 = df['Low'] - 2 * (df['High'] - PP)
    dataframe = pd.concat([PP,R1,S1,R2,S2], axis=1, keys= ["PP","R1","S1","R2","S2"])
    return dataframe

#Pivot Points, Supports and Resistances using Fibbonacci 
def FibboSR(df):  
    PP = (df['High'] + df['Low'] + df['Close']) / 3
    RangeHL = df['High'] - df['Low']

    S1 = PP - 0.382 * RangeHL
    S2 = PP - 0.618 * RangeHL
    S3 = PP - 1.0 * RangeHL
    
    R1 = PP - 0.382 * RangeHL
    R2 = PP - 0.618 * RangeHL
    R3 = PP - 1.0 * RangeHL

    dataframe = pd.concat([PP,R1,S1,R2,S2,R3,S3], axis=1, keys= ["PP","R1","S1","R2","S2","R3","S3"])
    return dataframe

def PSAR(df, iaf = 0.02, maxaf = 0.2):
    length = len(df)
    high = list(df['High'])
    low = list(df['Low'])
    close = list(df['Close'])
    
    psar = close[0:len(close)]
    psarbull = [np.NaN] * length
    psarbear = [np.NaN] * length
    bull = True
    af = iaf
    hp = high[0]
    lp = low[0]
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        reverse = False
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf
        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]
    
    dataframe = pd.DataFrame([psarbull,psarbear]).T
    dataframe.index = df.index
    dataframe.columns = ["Bull(%.2f,%.2f)"%(iaf,maxaf),"Bear(%.2f,%.2f)"%(iaf,maxaf)]
    return dataframe

