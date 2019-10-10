import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def set_zoom(self, axes = None, xlim = None ,X = None, Y = None, ylim = None, xpadding = None ,ypadding = None):
    """
    Function to allows to play with the zooming more easily. It allows sevral modes at the same time
    """
    if (type(axes) == type(None)):
        axes = self.axes
    if (type(Y) == type(None)):
        Y = self.Y[self.start_indx:self.end_indx]
    if (type(X) == type(None)):
        X = self.X[self.start_indx:self.end_indx]
        
    if ylim is not None:
        self.set_ylim(axes = axes, ymin = ylim[0], ymax = ylim[1])
    elif ypadding is not None:
        self.set_ylim_padding(axes = axes, Y = Y, padding = ypadding)

    if xlim is not None:
        self.set_xlim(axes = axes, xmin = xlim[0], xmax = xlim[1])
    elif ypadding is not None:
        self.set_xlim_padding(axes = axes, X = X, padding = xpadding)
        


def set_ylim_padding(self, axes = None, X = None, padding = [0.1, 0,1]):
        max_signal = np.max(X[~np.isnan(X)])
        min_signal = np.min(X[~np.isnan(X)])
        signal_range = max_signal - min_signal
        if (signal_range == 0):
            signal_range = max_signal
            if ( signal_range > 0):
                min_signal = 0
            else:
                max_signal = 0
        self.set_ylim(axes = axes, ymin = min_signal - signal_range* padding[0] , 
                      ymax = max_signal + signal_range*padding[1])
    

def set_xlim_padding(self, axes = None, Y = None, padding = [0.1, 0,1]):
        max_signal = np.max(Y[~np.isnan(Y)])
        min_signal = np.min(Y[~np.isnan(Y)])
        signal_range = max_signal - min_signal
        if (signal_range == 0):
            signal_range = max_signal
            if ( signal_range > 0):
                min_signal = 0
            else:
                max_signal = 0
        self.set_ylim(axes = axes, ymin = min_signal - signal_range* padding[0] , 
                      ymax = max_signal + signal_range*padding[1])
        
    
def set_xlim(self, ax = None, X = None, xmin = None, xmax = None):
    # This function sets the limits for viewing the x coordinate
    if (type(ax) == type(None)):
        ax = self.axes
    if (type(X) == type(None)):
        X = self.X[self.start_indx:self.end_indx]
        
    if (type(xmin) == type(None)):
        xmin = np.min(X[~np.isnan(X)])
    if (type(xmax) == type(None)):
        xmax = np.max(X[~np.isnan(X)])
        
        
    ax.set_xlim([xmin,xmax])

def set_ylim(self, ax = None, Y = None, ymin = None, ymax = None):
    # This function sets the limits for viewing the x coordinate
    
    if (type(Y) == type(None)):
        Y = self.Y[self.start_indx:self.end_indx]
        
    if (type(ax) == type(None)):
        ax = self.axes
    
    if (type(ymin) == type(None)):
        ymin = np.min(Y[~np.isnan(Y)])
    if (type(ymax) == type(None)):
        ymax = np.max(Y[~np.isnan(Y)])

        
    ax.set_ylim([ymin,ymax])

