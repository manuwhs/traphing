import numpy as np
from ...graph.Gl import gl

############# BASIC PLOTS #####################################
def plot_series(self, axes = None, series_name = "Close", *args, **kwargs):         
    time_series = self[series_name];
    timestamps = self.timestamps
    
    # TODO: Merge of dictionaries to be able to add properties externally
    labels = ["Price", "", ""]
    legend = [series_name]
    
    if (series_name == "Volume"):
        drawings =  gl.stem(timestamps,time_series, legend = legend, *args, **kwargs)
    else:
        drawings = gl.plot(timestamps,time_series, axes = axes, legend = legend, 
                           *args, **kwargs)
    return drawings

def plot_indicator(self, axes = None, indicator_name = "SMA", *args, **kwargs):         
    indicator_output = self.indicator(name = indicator_name, *args, **kwargs)
    timestamps = self.timestamps
    
    if indicator_name in ["SMA","EMA","WMA","HMA","HMAg"]:
        drawings = gl.plot(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    elif indicator_name in ["MOM","ROC","RETURN","GAP"]:
        drawings = gl.stem(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    elif indicator_name == "MACD":
        drawings = _plot_MACD(indicator_output, axes = axes, color_mode = 1)
    elif indicator_name in ["RSI"]:
        drawings = _plot_oscillator(indicator_output[indicator_output.columns[1]], axes = axes, color_mode = 1) 
    return drawings


def plot_barchart(self,*args, **kwargs):         
    if (self.df.shape[0] >0):
        drawings = gl.barchart(self.df,*args, **kwargs)
        return drawings


def plot_candlesticks(self, *args, **kwargs):         
    drawings = gl.candlestick(self.df,*args, **kwargs)
    return drawings

"""
######################## INTERNAL COMPLEX PLOTTING #############
"""

def _plot_MACD(MACD_df, axes = None, color_mode = 1):
    if (color_mode == 0):
        fillcolor = '#00ffe8'
        indCol = '#c1f9f7'
        posCol = '#386d13'; negCol = '#8f2020'
        bg_color = '#07000d'; col_axis = 'w'
        col_spines = "#5998ff"
    elif (color_mode == 1):
        fillcolor = '#00ffe8'
        indCol = '#c1f9f7'
        posCol = '#386d13'; negCol = '#8f2020'
        bg_color = '#07000d'; col_axis = 'k'
        col_spines = "#5998ff"
        
    timestamps = MACD_df.index
    MACD = MACD_df["MACD"]
    MACDsign= MACD_df["MACDsign"]
    MACDdiff= MACD_df["MACDdiff"]

    gl.plot(timestamps, MACD, axes=axes,color='#4ee6fd', lw=2)
    gl.plot(timestamps, MACDsign, axes = axes, color='#e1edf9', lw=1)
    gl.fill_between(timestamps, MACDdiff, axes = axes, y2 = 0, alpha=0.5) # facecolor=fillcolor, edgecolor=fillcolor)

    ## Format the axis
    gl.color_axis(axes, col_spines, col_axis)
#    axes.set_ylabel('MACD', color='k', fontsize = 15)

def _plot_oscillator(oscillator_series, axes = None, color_mode = 0):
    """
    Plots an oscillator, we need the series name
    """
    if (color_mode == 0):
        indCol = '#c1f9f7'
        posCol = '#386d13'; negCol = '#8f2020'
        bg_color = '#07000d'; col_axis = 'w'
        col_spines = "#5998ff"
        
    if (color_mode == 1):
        indCol = '#c1f9f7'
        posCol = '#386d13'; negCol = '#8f2020'
        bg_color = '#07000d'; col_axis = 'k'
        col_spines = "#5998ff"
        
    highline = 70
    lowline = 30
    
    timestamps = oscillator_series.index
    gl.plot(timestamps, oscillator_series, color = indCol, lw=1.5)

    if axes is None:
        axes = gl.axes
        
    # Draw some lines ! 
    axes.axhline(highline, color=negCol)
    axes.axhline(lowline, color=posCol)
    
    # Fill between the lines !
    # Since rsi has Nan, the inequalities will give a warning, but that is it.
#    warnings.filterwarnings("ignore")
    gl.fill_between(x = timestamps, y1 = oscillator_series, y2 = highline, alpha=0.99, 
                    where=(oscillator_series>=highline)) # facecolor=negCol, edgecolor=negCol
    gl.fill_between(x = timestamps, y1 = oscillator_series, y2 = lowline, alpha=0.99, 
                    where=(oscillator_series<=lowline)) # , facecolor=posCol, edgecolor=posCol
#    warnings.filterwarnings("always")
    
    ## Format color and so on.
    axes.set_yticks([lowline,highline])
    axes.yaxis.label.set_color(col_axis)
    gl.color_axis(axes, col_spines, col_axis)

    
############# Indicator plots #####################################

def scatter_deltaDailyMagic(self):
    ## PLOTS DAILY HEIKE ASHI
    ddelta = self.get_timeSeriesbyName("RangeCO")
    hldelta = self.get_timeSeriesbyName("RangeHL")
    
    mdelta = self.get_magicDelta()
    labels = ["Delta Magic Scatter","Magic","Delta"]

    gl.scatter(mdelta,ddelta, 
               labels = labels,
               legend = [self.symbolID],
               nf = 1)
    
#    gl.set_subplots(1,1)
    gl.scatter_3D(mdelta,ddelta, hldelta,
                   labels = labels,
                   legend = [self.symbolID],
                   nf = 1)

def plot_TrCrMr(self):
    ## Plots the Three deadly cross thingy.
    timeSeries = self.get_timeSeries()
    TrCrMr = self.get_TrCrMr()
    labels = ["Trio de la Muerte","Time","Price"]
    gl.plot(self.dates,timeSeries, 
                  labels = labels,
                  legend = ["Price"],
                  color = "k",nf = 1)
    
    gl.plot(self.dates,TrCrMr, 
                  labels = labels,
                  legend = ["Trio de la Muerte"],
                  color = "b",nf = 0)

def plot_BollingerBands(self, new_figure = 0, L = 21):
    if (new_figure == 1):
        self.new_plot(title = "Bollinger Bands", xlabel = "time", ylabel = "Close")
    
    SMA = self.get_SMA(L = L)
    BB = self.get_BollingerBand(L = L)
    
    self.plot_timeSeries()
    gl.plot(self.dates,SMA + BB, legend = ["SMA + BB"], nf = 0)
    gl.plot(self.dates,SMA - BB, legend = ["SMA - BB"], nf = 0)


