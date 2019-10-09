import matplotlib.pyplot as plt
from .. import utils as ul
from ..math import basicMathlib as bMl
import copy
from collections import OrderedDict
import pandas as pd

from .trapyngColors import cd
#####  BUILDING FUNCTIONS #####

def _update_legend(self, axes, n_drawings, legend = [], loc = "best"):
    # TODO: make something so that the legends do not overlap when we have shared axes.

    if(len(legend) > 0):
        self.legend.extend(legend)
    else:
        self.legend.extend(["Line"]*n_drawings)
        
#    self.axes.legend(self.legend, loc=loc)
#    l = plt.legend()
    if(len(legend) > 0):   
        if (axes.legend()):
#            ax.legend().set_zorder(0) # Set legend on top
            axes.legend(loc=loc)
    else:
        handles, labels = axes.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        axes.legend(by_label.values(), by_label.keys())
        

def format_legend(self, axes, handlelength=None, # Length of handle
                  handletextpad= None,   # Distance between handle and text
                  borderpad=None,        # Distance between border legend and content
                  labelspacing=None,     # Horizontal spacing between labels
                  borderaxespad= 0.1,
                  columnspacing = 0.1,
                  ncol=None              # Number of columns of the legend
                  ):
                      
    axes.legend(loc='best', handlelength=handlelength, borderpad=borderpad, 
              labelspacing=labelspacing, ncol=ncol, borderaxespad = borderaxespad, columnspacing = columnspacing)


def set_font_sizes(self, axes = None, title = None, xlabel = None, ylabel = None, 
                  legend = None, xticks = None, yticks = None):
                      
    if (type(axes) == type(list())):
        for ax_i in axes:
            self.set_fontSizes(axes = ax_i, title = title, xlabel = xlabel, ylabel = ylabel, 
                  legend = legend, xticks = xticks, yticks = yticks)
    else:
        # Set fontsize of the tittle
        if type(title) is not None:
            axes.title.set_fontsize(fontsize=title)
            
        # Set fontsize of the axis labels
        if xlabel is not None:
            axes.xaxis.label.set_size( fontsize = xlabel)
        if ylabel is not None:
            axes.yaxis.label.set_size( fontsize = ylabel)
            
        # Set the fontsize of the ticks
        if xticks is not None:
            for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(xticks) 
        if yticks is not None:
            for tick in axes.yaxis.get_major_ticks():
                tick.label.set_fontsize(yticks) 
        
        # Set the fontsize of the legend
        if (type(legend) != type(None)):
            axes.legend(fontsize=legend)    

            
def set_labels(self, axes, labels = ["title","x_label","y_label"]):
    if (len(labels) > 0):
        title = labels[0]
#        ax.title.set_text(title)
#        ax.title(title, y=1.01)
        axes.set_title(title, pad = 20)

    if (len(labels) > 1):
        xlabel = labels[1]
        axes.set_xlabel(xlabel)
        
    if (len(labels) > 2):
        ylabel = labels[2]
        axes.set_ylabel(ylabel)



def add_text(self, axes, x,y, text = r'an equation: $E=mc^2$',fontsize = 15):
    return axes.text(x, y, text, fontsize=fontsize)


