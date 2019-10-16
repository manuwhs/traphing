import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt 

import sys
sys.path.insert(0, "..") # Adds higher directory to python modules path.

from traphing.data_classes import Velas
from traphing.utils import Timeframes
from traphing.graph.Gl import gl

plt.close("all")

symbol_name = "AUDCHF"
timeframe = Timeframes.M15
storage_folder = "../tests/data/storage/"

velas = Velas(symbol_name, timeframe)
velas.load_data_from_csv(storage_folder)
start_time = dt.datetime(2019,8,14); end_time = dt.datetime(2019,8,18)
velas.set_time_interval(start_time, end_time)
timestamps = velas.timestamps

"""
    Moving averages
"""

if(0):
    indicators_name = ["SMA","EMA","WMA","HMA","HMAg"]
    indicators_args = [{"n":20, "series_name":"Close"}, {"n":40}, {},{},{}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
    close = velas.series("Close")
    gl.plot(timestamps, close, axes = axes_all, legend = [close.name])
    
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.Series)
        assert indicator_output.index[0] == velas.df.index[0]
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all, sharey = axes_all)
        gl.plot(timestamps, indicator_output, axes = axes_all, legend = [indicator_output.name])
        gl.plot(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)


"""
    Supports and Resistances
"""

if(0):
    indicators_name = ["PPSR","FibboSR", "PSAR", "BBANDS"]
    indicators_args = [{}, {}, {}, {}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
     
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        print (indicator_output)
    #    assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.DataFrame)
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all, sharey = axes_all)
        gl.plot(timestamps, indicator_output, axes = axes_all, legend = indicator_output.columns)
        gl.plot(timestamps, indicator_output, axes = axes, legend = indicator_output.columns)
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)


"""
    Momentum 
"""
if(0):
    indicators_name = ["MOM","ROC", "RETURN"]
    indicators_args = [{}, {}, {}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
     
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        print (indicator_output)
    #    assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.Series)
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all, sharey = axes_all)
        gl.stem(timestamps, indicator_output, axes = axes_all, legend = [indicator_output.name])
        gl.stem(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)
    
    
"""
    Ranges 
"""
if(0):
    indicators_name = ["STD","AHLR", "ATR", "Chaikin_vol", "GAP"]
    indicators_args = [{}, {}, {}, {}, {}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
     
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        print (indicator_output)
    #    assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.Series)
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all)
        gl.plot(timestamps, indicator_output, axes = axes_all, legend = [indicator_output.name])
        gl.plot(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)

"""
    Oscillators 
"""
if(0):
    indicators_name = ["STO","MACD","TRIX","RSI"]
    indicators_args = [{}, {}, {}, {}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
     
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        print (indicator_output)
    #    assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.DataFrame)
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all)
        gl.plot(timestamps, indicator_output, axes = axes_all, legend = indicator_output.columns)
        gl.plot(timestamps, indicator_output, axes = axes, legend = indicator_output.columns)
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)
    

"""
Volume
"""
if(0):
    indicators_name = ["ACCDIST"]
    indicators_args = [{}, {}, {}, {}]
    
    gl.init_figure()
    n_rows = len(indicators_name)
    n_cols = 2
    
    axes_all = gl.subplot2grid((n_rows, n_cols), (0,0), rowspan = n_rows)
     
    for i in range(len(indicators_name)):
        name = indicators_name[i]
        args = indicators_args[i]
        indicator_output = velas.indicator(name, **args)
        
        print (name, ": ", type(indicator_output))
        print (indicator_output)
    #    assert indicator_output.shape == (velas.df.shape[0],)
        assert isinstance(indicator_output, pd.Series)
        
        axes = gl.subplot2grid((n_rows, n_cols), (i,1), sharex = axes_all)
        gl.plot(timestamps, indicator_output, axes = axes_all, legend = [indicator_output.name])
        gl.plot(timestamps, indicator_output, axes = axes, legend = [indicator_output.name])
    
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True)
    

