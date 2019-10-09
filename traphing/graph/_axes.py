import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def _manage_axes(self, axes = None, position = [], 
                sharex = None, sharey = None, projection = "2d"):
                    
    """This function manages the creation of the new axes
    or the reusing of the previous one.
    """
    
    if (type(axes) == type(None)):    
        axes  = self.create_axes(position = position, projection = projection,
                               sharex = sharex, sharey = sharey)# Self.axes is the last axes we do stuff in
    self._add_axes(axes)
    return axes


def _add_axes(self, axes):
    """ Adds the axes to our interval list axes_list and sets it as 
    the latest ax to plot in. This is actually done as well by plt
    """
    self.axes = axes
    self.axes_list.append(axes)
    
    
def _twin_axes(self, axes = None):
    """ Creates a twin axes and modifies the interval structures
    """
    if (type(axes) == type(None)):
        axes = self.axes
    axes = axes.twinx()  # Create a twin axis
    self._add_axes(axes)
    return axes

def create_axes(self, position = [0.1, 0.1, 0.8, 0.8] , projection = "2d",
                sharex = None, sharey = None):
    """
    Create axes with different posibilities
    """
    if (self.figure == None):       # If there is no figure
        self.init_figure()
    if (projection == "2d"):
        axes = plt.axes( ) # position = position
#        axes = self.figure.add_axes()
    elif (projection == "3d"): # No really need, since the 3D func create axis anyway
        axes = plt.axes(projection='3d')  # Or plt.plot
    elif ( projection == "polar"):
        axes = self.fig.add_axes(position, projection = projection)
    else:
        print ("No valid projection")
        
    self._add_axes(axes)
    return axes


def get_axes(self):
    return self.axes_list



