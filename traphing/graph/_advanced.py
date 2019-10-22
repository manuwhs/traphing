import numpy as np
import matplotlib.pyplot as plt
from .. import utils as ul
import copy

from matplotlib.patches import Rectangle
import datetime as dt
from matplotlib import collections  as mc
from matplotlib.lines import Line2D

def barchart(self, df, labels = [], legend = [],  color = None,  lw = 1, alpha = 1.0,  # Basic line properties
        axes = None, position = [], projection = "2d", sharex = None, sharey = None,
        font_sizes = None,axis_style = None, loc = "best",
        xlim = None, ylim = None, xpadding = None, ypadding = None, # Limits of vision
        ws = None,init_x = None,
        
       ):         
           
    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, df.index, df["High"], None, ws)
    
    High,Low, Open,Close = df["High"],df["Low"],df["Open"],df["Close"]
    n_samples = X.size

    X = ul.to_mdates(X)
    width_unit = self._get_barwidth(X)
    
    dist = width_unit /2.2
    
    X_prev =  [X[i] - dist for i in range(X.size)]
    X_post = [X[i] + dist for i in range(X.size)]
    X = [X[i] for i in range(X.size)]
    
    linesHL = [[(X[i],Low[i]),(X[i], High[i])] for i in range(n_samples)]
    linesO = [[(X_prev[i],Open[i]),(X[i], Open[i])] for i in range(n_samples)]
    linesC = [[(X[i],Close[i]),(X_post[i], Close[i])] for i in range(n_samples)]

#    print mdates.date2num(X[i,0].astype(dt.datetime)), type(mdates.date2num(X[i,0].astype(dt.datetime))) 
    self.zorder = self.zorder + 1  # Setting the properties
    colorFinal = self.get_color(color)
    
    # TODO: Handle the legend better
    if len(legend)>0:
        label_legend = legend[0]
    else:
        label_legend = None
        
    lcHL = mc.LineCollection(linesHL, colors= colorFinal, linewidths=lw, antialiased=True, label = label_legend)
    lcO = mc.LineCollection(linesO, colors= colorFinal, linewidths=lw, antialiased=True)
    lcC = mc.LineCollection(linesC, colors= colorFinal, linewidths=lw, antialiased=True)
    axes.add_collection(lcHL)
    axes.add_collection(lcO)
    axes.add_collection(lcC)
    axes.autoscale()  # TODO: The zoom is not changed if we do not say it !

    self._postdrawing_settings(axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,axis_style,X,Y)

def histogram(self, X,  bins = 20, orientation = "vertical",
        *args, **kwargs):   
             
    hist, bin_edges = np.histogram(X, density=True, bins = bins)
    self.bar(bin_edges[:-1], hist, orientation = orientation,*args, **kwargs)


#    if (orientation == "vertical"):
#        self.plot(x_grid, y_values, nf = 0, *args, **kwargs)
#    else:
#        self.plot(y_values, x_grid, nf = 0, *args, **kwargs)

def candlestick(self, df, labels = [], legend = [],  color = None,  lw = 1, alpha = 1.0,  # Basic line properties
        axes = None, position = [], projection = "2d", sharex = None, sharey = None,
        font_sizes = None,axis_style = None, loc = "best",
        xlim = None, ylim = None, xpadding = None, ypadding = None, # Limits of vision
        ws = None,init_x = None,
        
        ## Specific 
        lw2 = 2
       ):     

    colorInc = 'blue'
    colorDec = "red"
    color_range = "black"
    
    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, df.index, df["High"], None, ws)
    
    High,Low, Open,Close = df["High"],df["Low"],df["Open"],df["Close"]
    n_samples = X.size

    incBox = []
    decBox = []
    allBox = []
    # Calculate upper and lowe value of the box and the sign
    for i in range(n_samples):
        diff = Close[i] - Open[i]
    #        print diff
        if (diff >= 0):
            incBox.append(i)
        else:
            decBox.append(i)
        allBox.append(i)
    
#    X = ul.to_mdates(X)
    barwidth = self._get_barwidth(ul.to_mdates(X))
    print(barwidth)
    ## All range bars !!
    self.bar(X[allBox], np.array(High[allBox] - Low[allBox]), bottom = np.array(Low[allBox]),
             barwidth = barwidth*0.1, color = color_range, axes = axes)  
             
#    self.bar(X[allBox], np.abs(Open[allBox] - Close[allBox]), 
#             bottom =np.min(np.array([Close[allBox],Close[allBox]]).T, axis =1),
#             barwidth = barwidth*0.9, color = colorDec)

#    ## Increasing bars !!
    self.bar(X[incBox], np.array(Close[incBox] - Open[incBox]), bottom = np.array(Open[incBox]),
             barwidth =barwidth*0.9, color = colorInc, axes = axes)
#    ## Decreasing bars !!
    self.bar(X[decBox], np.array(Open[decBox] - Close[decBox]), bottom = np.array(Close[decBox]),
             barwidth = barwidth*0.9, color = colorDec, axes = axes)

def Heiken_Ashi_graph(self, data, labels = [], nf = 1):
    r_close = data["Close"].values
    r_open = data["Open"].values
    r_max = data["High"].values
    r_min = data["Low"].values
    x_close  = (r_close + r_open + r_max + r_min)/4
    x_open = (r_close[1:] + x_close[:-1])/2  # Mean of the last 
    
    # Insert the first open sin we cannot calcualte the prevoius
    # The other opion is to eliminate the first of everyone
    x_open = np.insert(x_open, 0, r_open[0], axis = 0)
    
#    print x_close.shape, x_open.shape
    x_max = np.max(np.array([r_max,x_close,x_open]), axis = 0)
    x_min = np.min(np.array([r_min,x_close,x_open]), axis = 0)
    
    
    ### Lets create another pandas dataframe with this data
    new_data = copy.deepcopy(data)
    new_data["Close"] = x_close
    new_data["Open"] = x_open
    new_data["High"] = x_max
    new_data["Low"] = x_min
    
    self.Velero_graph(new_data, labels = [], nf = 1)
    
#    x_close  = np.mean(data,0)
#    x_open = data[0][1:] + upper_box[:-1]  # Mean of the last 

def plot_timeSeriesRange(self, X, Y, sigma, k = 1.96, nf = 0, legend = ["95% CI f(x)"]):
    # Plots the time series with its 1.96 percent interval
    gl = self
    gl.plot(X,Y, nf = 0,legend = legend)
    gl.plot_filled(X, np.concatenate([Y - 1.9600 * sigma,
           Y + 1.9600 * sigma],axis = 1), alpha = 0.5, nf = 0)
    
def plot_timeRegression(self,Xval, Yval, sigma,
                        Xtr, Ytr,sigma_eps = None, 
                        labels = ["Gaussian Process Estimation","Time","Price"], nf = 0):
    # This is just a general plotting funcion for a timeSeries regression task:
    # Plot the function, the prediction and the 95% confidence interval based on
    # the MSE
    # eps is the estimated noise of the training samples.
    """
    sigma is the std of each of the validation samples 
    sigma_eps is the considered observation noise
    """
    
    Xval = ul.fnp(Xval)
    Yval = ul.fnp(Yval)
    Xtr = ul.fnp(Xtr)
    Ytr = ul.fnp(Ytr)

    sigma = ul.fnp(sigma)
    sigma_eps = ul.fnp(sigma_eps)
    
    gl = self
    gl.plot(Xval,Yval, labels = labels, legend = ["Estimated Mean"], nf = nf)
    
    gl.plot_filled(Xval, np.concatenate([Yval - 1.9600 * sigma,
           Yval + 1.9600 * sigma],axis = 1), alpha = 0.5, legend = ["95% CI f(x)"])
    
    # If we are given some observaiton noise we also plot the estimation of it
    if type(sigma_eps) != type(None):
        # Ideally we have a func that tells us for each point, what is the observation noise.
        # We are suposed to know what is those values for training, 
        # TODO: And for testing ? Would that help ? I think we are already assuming so in the computation of K.
        # The inner gaussian process can also be specified "alpha", we will research more about that later.
        # I guess it is for hesterodasticity.
        # We are gonna consider that the observation noise of the predicted samples is homocedastic.
        sigma = np.sqrt(sigma**2 + ul.fnp(sigma_eps)[0]**2)
        # TODO: maybe in the future differentiate between sigma_eps and dy
        gl.plot_filled(Xval, np.concatenate([Yval - 1.9600 * sigma,
               Yval + 1.9600 * sigma],axis = 1), alpha = 0.2, legend = ["95% CI y(x)"])
                       
    # TODO: what is this     ec='None'

    if type(sigma_eps) != type(None):
        if (ul.fnp(sigma_eps).size == 1):
            sigma_eps = np.ones((Xtr.size,1)) * sigma_eps
        plt.errorbar(Xtr.ravel(), Ytr, sigma_eps, fmt='k.', markersize=10, label=u'Observations')
    else:
        gl.scatter(Xtr, Ytr, legend = ["Training Points"], color = "k")
        