import matplotlib.pyplot as plt
from .. import utils as ul
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
#####  BUILDING FUNCTIONS #####

#from matplotlib.ticker import FuncFormatter

def format_axis(self, axes, axis_style):
    self.format_xaxis(axes)
    self.format_yaxis(axes)
    self.apply_axis_style(axes, axis_style)
    
def format_xaxis (self, axes, 
                  n_ticks = 10,    # Number of ticks we would like
                  timestamp_formatting = '%Y-%m-%d:%H:%M',  # Specified formatting 
                  xaxis_mode = None): # Several automatic modes 
    """
    Handle all possible tailoring of the x_axis
    """
    if (self.X_type == "categorical"):
        axes.set_xticks(self.X[self.start_indx:self.end_indx], minor=False)
        axes.set_xticklabels(self.Xcategories[self.start_indx:self.end_indx][:,0], minor=False)
        
    elif(self.X_type == "numerical"):
        # If regular numerical we just plot the values
        axes.xaxis.set_major_locator(mticker.MaxNLocator(nbins = n_ticks,  prune='upper'))
#        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        
    elif(self.X_type == "timestamp"):
        axes.xaxis.set_major_formatter(mdates.DateFormatter(timestamp_formatting))
        axes.xaxis.set_major_locator(mticker.MaxNLocator(nbins = n_ticks,  prune='upper'))
        axes.xaxis_date()
      #  ax.xaxis.set_major_formatter(FuncFormatter(self.ticklabels[val:val + wsize]))
      
    elif(self.formatXaxis == "intraday"):
        # If the data is intraday and we want to apply the Gap Remover !!! 
        gap_remover_flag = 1;
        if (gap_remover_flag):
            formatter = FuncFormatter(ul.detransformer_Formatter)
            axes.xaxis.set_major_formatter(formatter)  
            # mdates.DateFormatter(formatting)
            
        else:
            axes.xaxis.set_major_formatter(mdates.DateFormatter(formatting))
        
        axes.xaxis.set_major_locator(mticker.MaxNLocator(nbins = n_ticks,  prune='upper'))
        
def format_yaxis(self, axes):
    pass

def apply_axis_style(self, axes, axis_style = None):
    """
    This function applies standard specfied formattings :)
      - Normal: Normal colors, texts, sizes...
      - Educational: Big arrow in the center for X and Y axis
    
    """
#    self.axes.grid(True)
    
    if axis_style == "Normal":
        self.set_fontSizes(title = 20, xlabel = 20, ylabel = 20, 
              legend = 20, xticks = 11, yticks = 13)
        self.set_textRotations(xticks = 60)
        self.color_axis(color_spines = "k", color_axis = "k")
        self.format_xaxis (Nticks = 20,formatting = None)
        self.format_legend(handlelength=1.5, borderpad=0.5,labelspacing=0.3, ncol = 2)
        
        if axes.get_legend() is not None:     
            self.axes.get_legend().get_title().set_fontsize(25)

    elif axis_style == "Educational":
        self.set_fontSizes(title = 20, xlabel = 20, ylabel = 20, 
                  legend = 20, xticks = 15, yticks = 15)
        self.format_xaxis (Nticks = 10,formatting = None)
        self.format_legend(handlelength=1.5, borderpad=0.5,labelspacing=0.3, ncol = 2)
        if (type( self.axes.get_legend()) != type(None)):     
            self.axes.get_legend().get_title().set_fontsize(25)
        
        axes.axhline(linewidth=1.7, color="black",marker = ">",ms = 6)
        axes.axhline(linewidth=1.7, color="black",marker = "<")
        axes.axvline(linewidth=1.7, color="black",marker = "^")
        axes.axvline(linewidth=1.7, color="black",marker = "v")

        
def color_axis(self, axes, color_spines = "w", color_axis = "w"):
    if axes is None:
        axes = self.axes
        
    axes.set_facecolor('k')
    axes.spines['bottom'].set_color(color_spines)
    axes.spines['top'].set_color(color_spines)
    axes.spines['left'].set_color(color_spines)
    axes.spines['right'].set_color(color_spines)
    axes.yaxis.label.set_color(color_axis)
    axes.tick_params(axis='y', colors=color_axis)
    axes.tick_params(axis='x', colors=color_axis)


def hide_xaxis(self, axes):
    plt.setp(axes.get_xticklabels(), visible=False)


def hide_yaxis(self, axes):
    plt.setp(axes.get_yticklabels(), visible=False)
    

def set_xticks_rotation(self, axes, degree = None):
    if (degree is not None):
        for label in axes.xaxis.get_ticklabels():
            label.set_rotation(degree)
            
            
def set_yticks_rotation(self, axes, degree = None):
    if (degree is not None):
        for label in axes.yaxis.get_ticklabels():
            label.set_rotation(degree)
            
            