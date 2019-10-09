import matplotlib.pyplot as plt
from .. import utils as ul
from ..math import basicMathlib as bMl
import copy
from collections import OrderedDict
import pandas as pd

from .trapyngColors import cd
#####  BUILDING FUNCTIONS #####

def _predrawing_settings(self, axes, sharex, sharey,
                 position,  projection, X,Y, dataTransform, ws):
    axes = self._figure_management(axes = axes, sharex = sharex, sharey = sharey,
                     position = position,  projection = projection)
    X, Y = self._preprocess_data(X,Y, dataTransform = dataTransform)
    drawings,drawings_type =  self._init_WidgetData(ws)

    return axes, X,Y, drawings,drawings_type

def _postdrawing_settings(self,axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,X,Y):
    
    self._update_legend(legend,axes = axes, loc = loc)
    self.set_labels(labels)
    self.set_font_sizes(font_sizes)
    self.format_axis()
    self.set_zoom(axes,xlim,X,Y,ylim,xpadding,ypadding)
        
def get_color(self, color = None):
    """
    This function outputs the final color to print for a given plotting
    """
    
    if (type(color) == type(None)):
        # If no color specified. We use one of the list
        colorFinal = self.colors[self.colorIndex]
        self.colorIndex = (self.colorIndex + 1) %len(self.colors)
        
    elif(type(color) == type([])):
        colorFinal = color
    else:
        if(color in cd.keys()):
            colorFinal = cd[color]
        else:
            colorFinal = color
    return colorFinal
    


