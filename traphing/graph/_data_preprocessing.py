import matplotlib.pyplot as plt
from .. import utils as ul
from ..math import basicMathlib as bMl
import copy
from collections import OrderedDict
import pandas as pd
import numpy as np
import datetime as dt

from .trapyngColors import cd
    
def _preprocess_data(self,X,Y, dataTransform = None ):
    """
    Function that processes X and Y  into a format that matplotlib can understand.
    For each axis (x and y) we have 2 vectors:
        - Vector of data: 
            X and Y which are a transformation of the original data into 
            a common format:
              - numerical: Numpy array
              - categorical: Integers starting at 0
              - timestamps: XXX matplotlib dates? 
        - Vector of labels: 
            X_ticks and Y_ticks are the tags of each of the values in X and Y 
            respectively. This is mainly for categorical values, it will contain them.
    """
    self.X, self.X_ticks, self.X_type = _format_data_to_plotting_type(X)
    self.Y, self.Y_ticks, self.Y_type  = _format_data_to_plotting_type(Y)

    return self.X, self.Y

def _format_data_to_plotting_type(data):
    """
    Format X data for the being printed by the matplotlib library.
    The data generated should be easily digestable by the matplotlib library functions
    
    If the data is simply numeric:
        - It returns a number 2 numpy dimensional array (Nsamples, Nsignals)
    
    If the data is categorical:
        -
    If the data are datetimes (matplotlib, pandas, numpy, datetime, time)
        - It transforms them to [Nsam, 1] numpy.ndarray with elements being numpy.datetime64 or pd.datetime. not sure
        The final transformation to matplotlib dates is done in the axis formatting part.
        The self.X is never modified, it contains the original data to be able to operate with it.
    """
    data_ticks = None
    
    if (ul.is_numerical_array(data)):
        data = ul.to_numpy_2d(data)
        data_type = "numerical"
        
    elif (ul.is_timestamp_array(data)):
        data = pd.to_datetime(data)
        data = ul.to_numpy_2d(data)
        data_type = "timestamp"
        
    elif(ul.is_categorical(data)):
        data_ticks = data
        data = ul.to_numpy_2d(range(data.size))
        data_type = "categorical"
    else:
        raise Warning("Not handled data type: " + str(type(data)))
    return data, data_ticks, data_type


def _get_barwidth(self,X):
    """
    X should be int or float.
    If X was originally dates, it should have been transformed to matplotlib mdates,
    before hitting this function
    """
    if (len(X.shape)>1):
        X = X.flatten()
    if ((type(X[0]).__name__ == "Timestamp" ) or (type(X[0]).__name__ == "datetime64" )):
        raise Warning("Convert the datetime object into matplotlib dates before calling get_barwidth")
    else:
        width = min(bMl.diff(X)[1:]) 
    return float(width)
    

def _format_data_axis(dataTransform):
    """
    Function to format the data to show
    """
    if (type(dataTransform) != type(None)):
        if (dataTransform[0] == "intraday"):
            # In this case we are going to need to transform the dates.
            openhour = dataTransform[1] 
            closehour = dataTransform[2]
            self.formatXaxis = "intraday"
            # Virtual transformation of the dates !
            self.Xcategories = self.X
            
            transfomedTimes = ul.transformDatesOpenHours(X,openhour, closehour )
            Mydetransfromdata = ul.deformatter_data(openhour, closehour, None)
            # Setting the static object of the function
            ul.detransformer_Formatter.format_data = Mydetransfromdata
            self.X = ul.fnp(transfomedTimes) 
            

