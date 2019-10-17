import numpy as np
from scipy import spatial
from . import sort_and_get_order
import pandas as pd

def check_crossing(reference, crosser):
    """
    It checks if one signal crosses the other.
    """
    detected = np.nan_to_num(np.diff(np.sign(reference - crosser)),0)
    idx_upwards = np.argwhere(detected < 0).flatten() +1 # +1 to be on the right-hand sample
    idx_downwards = np.argwhere(detected > 0).flatten() +1
    
    series = pd.Series(np.zeros((reference.shape[0])), index = reference.index, name = "Crosses")
    series[idx_upwards] = 1
    series[idx_downwards] = -1
    return series

def simmilarity(patterns,query,algo):
    # This funciton computes the similarity measure of every pattern (time series)
    # with the given query signal and outputs a list of with the most similar and their measure.

    Npa,Ndim = patterns.shape
    sims = []
    if (algo == "Correlation"):
        for i in range(Npa):
            sim =  np.corrcoef(patterns[i],query)[1,0]
            sims.append(sim)
        sims = np.array(sims)
        sims_ored, sims_or = sort_and_get_order (sims, reverse = True )
        
    if (algo == "Distance"):
        sims = spatial.distance.cdist(patterns,np.matrix(query),'euclidean')
        sims = np.array(sims)
        sims_ored, sims_or = sort_and_get_order (sims, reverse = False )
    return sims_ored, sims_or

    
def get_Elliot_Trends (yt, Nmin = 4, Noise = -1):
    
    Nsamples, Nsec = yt.shape
    if (Nsec != 1):
        print ("Deberia haber solo una senal temporal")
        return -1;
        
#    yt = yt.ravel()
    
#    yt = np.array(yt.tolist()[0])
    
    print (yt.shape)
    trends_list = []   # List of the trends
    
    support_t = 0   # Support index
    trend_ini = 0   # Trend start index

    support = yt[support_t]  # If support is broken then we dont have trend
    

    """ UPPING TRENDS """    
    for i in range (1,Nsamples-1):
        if (Noise == -1):
            tol = support/200
            
        #### Upper trends
        if (yt[i] > support- tol): # If if is not lower that the last min
            if (yt[i +1 ] < yt[i] - tol):  # If it went down, we have a new support
                support_t = i
                support = yt[support_t]
            
        else:   # Trend broken
            
            if ((i -1 - trend_ini) > Nmin): # Minimum number of samples of the trend
                trends_list.append([trend_ini, i -1])  # Store the trend
            
            # Start over
            trend_ini = i
            support_t = i
            support = yt[support_t]
    
    """ Lowing TRENDS """  
    
    for i in range (1,Nsamples-1):
        if (Noise == -1):
            tol = support/200
            
        #### Upper trends
        if (yt[i] < support + tol): # If if is not lower that the last min
            if (yt[i + 1] > yt[i] + tol):  # If it went up, we have a new support
                support_t = i
                support = yt[support_t]
            
        else:   # Trend broken
            
            if ((i - trend_ini) > Nmin): # Minimum number of samples of the trend
                trends_list.append([trend_ini, i -1])  # Store the trend
            
            # Start over
            trend_ini = i
            support_t = i
            support = yt[support_t]
    return trends_list
        

def support_detection(sequence, L):
    # This fuction get the support of the last L signals
    Nsamples, Nsec = sequence.shape
    
    sequence_view = sequence[-L:]
    index_min = np.argmin(sequence_view)
    
    return index_min + Nsamples - L 

def get_grids(X_data, N = [10]):
    # This funciton outputs the grids  of the given variables.
    # N is the number of points, if only one dim given, it is used to all dims
    # X_data = [Nsam][Nsig]
    Nsa, Nsig = X_data.shape
    
    ranges = []
    for i in range(Nsig):
        # We use nanmin to avoid nans
        ranges.append([np.nanmin(X_data[:,i]),np.nanmax(X_data[:,i])])
    
    grids = []
    for range_i in ranges:
        grid_i = np.linspace(range_i[0], range_i[1], N[0])
        grids.append(grid_i)
    
    return grids

def scale(X, absmax = 1):
    maxim = np.nanmax(np.abs(X))
    ret = X/maxim
    return ret
    