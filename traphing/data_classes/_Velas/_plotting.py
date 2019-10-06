
import numpy as np
import datetime as dt
from ...graph.Gl import gl

############# BASIC PLOTS #####################################

def plot_series(self, series_name = "Close", *args, **kwargs):         
    time_series = self[series_name];
    timestamps = self.timestamps
    
    if (series_name == "Volume"):
        ax =  gl.scatter(timestamps,time_series, *args, **kwargs)
    else:
        ax = gl.plot(timestamps,time_series, *args, **kwargs)
    return ax

def plot_barchart(self,*args, **kwargs):         
    timestamps = self.timestamps
    data_HLOC = np.array(self.df[["High","Low","Open","Close"]])
    print(data_HLOC)
    ax = gl.barchart(timestamps, data_HLOC,*args, **kwargs)
    return ax

def plot_candlesticks(self, *args, **kwargs):         
    data_OCHL = self.df[["Open","Close","High","Low"]]
    timestamps = self.timestamps    
    ax = gl.candlestick(timestamps, data_OCHL,*args, **kwargs)
    return ax

def plot_OCHL(self, chart_type = "Line", ax = None, dataTransform = None):
    df = self.df
    symbol_name = self.symbol_name
    timeframe_name = self.timeframe.name
    
    title = chart_type + " chart: " + str(symbol_name) + "(" + timeframe_name + ")"
    if (chart_type == "Line"):
        plot_series(df,  seriesName = "Close", ax = ax, 
                    legend = ["Close price"],labels = [title,"",r"Price ($\$$)"], 
                    AxesStyle = "Normal - No xaxis", dataTransform = dataTransform)
                    
    elif(chart_type == "Bar"):
         gl.tradingBarChart(df, ax = ax,  legend = ["Close price"], color = "k",
                            labels = [title,"",r"Price ($\$$)"], AxesStyle = "Normal - No xaxis", 
                            dataTransform = dataTransform)
    
    elif(chart_type == "CandleStick"):
         gl.tradingCandleStickChart(df, ax = ax,  legend = ["Close price"], color = "k",
                            colorup = "r", colordown = "k", alpha = 0.5, lw = 3,
                            labels = [title,"",r"Price ($\$$)"], AxesStyle = "Normal - No xaxis",
                             dataTransform = dataTransform)
         
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

######################################################################
############# Moving Averages Graph #######################################
######################################################################

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


