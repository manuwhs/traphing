import matplotlib.pyplot as plt
from .. import utils as ul

# The common properties will be explained here once and shortened in the rest
def plot(self, X = None,Y = None,           # X-Y points in the graph.
        labels = [], legend = [],       # Basic Labelling
        color = None,  lw = 2, alpha = 1.0,  # Basic line properties
        
        ## Axes options
        axes = None,      # Axes where this will be plotted. If none, it will be the last one.
        position = None,   # If given it will create a new axes [x,y,w,h]
        sharex = None, sharey = None, # When nf = 1, we are creating a new figure and we can choose
                                     # that new axes share the same x axis or yaxis than another one.
        projection = "2d", # Type of plot
        
        # Advanced fonts
        font_sizes = None,   # This is the fontsizes of [tittle, xlabel and ylabel, xticks and yticks]

        # Layout options
        xpadding = None, ypadding = None, # Padding in percentage of the plotting, it has preference
        xlim = None, ylim = None, # Limits of vision
        
        ### Special options 
        fill_between = False,  #  0 = No fill, 1 = Fill and line, 2 = Only fill
        alpha_line = 1, # Alpha of the line when we do fillbetween
        fill_offset = 0,  # The 0 of the fill
        ls = "-",
        marker = [None, None, None], # [".", 2, "k"],
        
        # Axis options
        axis_style = None,  # Automatically do some formatting :)

        ## Widget options
        ws = None,      # Only plotting the last window of the data.
        init_x = None,   # Initial point to plot
        # Basic parameters that we can usually find in a plot
        loc = "best",    # Position of the legend
        ):       

    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, X,Y, None, ws)
    
    for i in range(Y.shape[1]):  
        self.zorder+= 1  # 
        colorFinal = self.get_color(color)
        legend_i = None if i >= len(legend) else legend[i]
        alpha_line = alpha if fill_between == 0 else alpha_line
        
        drawing, = axes.plot(X[self.start_indx:self.end_indx],Y[self.start_indx:self.end_indx:,i], 
                 lw = lw, alpha = alpha_line, color = colorFinal,
                 label = legend_i, zorder = self.zorder,
                 ls = ls, marker = marker[0], markersize = marker[1], markerfacecolor = marker[2])
        drawings.append(drawing); drawings_type.append("plot")

        if (fill_between == True):  
            drawing = self.fill_between(x = X[self.start_indx:self.end_indx],
                              y1 = Y[self.start_indx:self.end_indx,i],
                              y2 = fill_offset, color = colorFinal,alpha = alpha)
            
    self._postdrawing_settings(axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,axis_style,X,Y)
    return drawings

def scatter(self, X = [],Y = [], labels = [], legend = [],  color = None,  lw = 1, alpha = 1.0,  # Basic line properties
        axes = None, position = [], projection = "2d", sharex = None, sharey = None,
        font_sizes = None,axis_style = None, loc = "best",
        xlim = None, ylim = None, xpadding = None, ypadding = None, # Limits of vision
        ws = None,init_x = None,
        ## Scatter specific
        marker = "o"
       ):         
    
    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, X,Y, None, ws)
    
    for i in range(Y.shape[1]):  # We plot once for every line to plot
        self.zorder = self.zorder + 1  # Setting the properties
        colorFinal = self.get_color(color)
        legend_i = None if i >= len(legend) else legend[i]
        drawing =  axes.scatter(X,Y, lw = lw, alpha = alpha, color = colorFinal,
                    label = legend_i, zorder = self.zorder, marker = marker)
        # TODO: marker = marker[0], markersize = marker[1], markerfacecolor = marker[2]
        drawings.append(drawing); drawings_type.append("scatter")
            
    self._postdrawing_settings(axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,axis_style,X,Y)
    return drawing


def stem(self, X = [],Y = [], labels = [], legend = [],  color = None,  lw = 2, alpha = 1.0,  # Basic line properties
        axes = None, position = [], projection = "2d", sharex = None, sharey = None,
        font_sizes = None,axis_style = None, loc = "best",
        xlim = None, ylim = None, xpadding = None, ypadding = None, # Limits of vision
        ws = None,init_x = None,
        ## Stem specific
        marker = [" ", None, None], 
        bottom = 0
       ):         

    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, X,Y, None, ws)
    
    ############### CALL PLOTTING FUNCTION ###########################
    for i in range(Y.shape[1]):  # We plot once for every line to plot
        self.zorder = self.zorder + 1  # Setting the properties
        colorFinal = self.get_color(color)
        legend_i = None if i >= len(legend) else legend[i]
        markerline, stemlines, baseline = axes.stem(X,Y[:,i], 
                use_line_collection = True,
                 label = legend_i,#marker[2],
                  bottom = bottom)
        
        # properties of the baseline
        plt.setp(baseline, 'color', 'r', 'linewidth', 1)
        plt.setp(baseline, visible=False)
        # properties of the markerline
        plt.setp(markerline, 'markerfacecolor',colorFinal)
        plt.setp(markerline, 'color',colorFinal)
        plt.setp(markerline, visible=False)
        # Properties of the stemlines
        plt.setp(stemlines, 'linewidth', lw)
        plt.setp(stemlines, 'color', colorFinal)
        plt.setp(stemlines, 'alpha', alpha)

        drawings.append([markerline, stemlines, baseline]); drawings_type.append("scatter")
            
    self._postdrawing_settings(axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,axis_style,X,Y)
    
    return [markerline, stemlines, baseline]

def fill_between(self, x, y1,  y2 = 0, where = None,
        labels = [], legend = [],  color = None,  lw = 2, alpha = 1.0,  # Basic line properties
        axes = None, position = [], projection = "2d", sharex = None, sharey = None,
        font_sizes = None,axis_style = None, loc = "best",
        xlim = None, ylim = None, xpadding = None, ypadding = None, # Limits of vision
        ws = None,init_x = None
        ):

    axes, X,Y, drawings,drawings_type = self._predrawing_settings(axes, sharex, sharey,
                 position,  projection, x,y1, None, ws)
    
    y1 = ul.fnp(Y).T.tolist()[0]

    if (where is not None):
        where = ul.fnp(where)
#        where = np.nan_to_num(where)
        where = where.T.tolist()[0]

    y2 = ul.fnp(y2)
    if (y2.size == 1):
        y2 = y2[0,0]
    else:
        y2 = y2.T.tolist()[0]
    
    drawing = axes.fill_between(x = X.flatten(), y1 = y1, y2 = y2, where = where,
                     color = color, alpha = alpha, zorder = self.zorder, label = legend) #  *args, **kwargs) 

    drawings.append(drawing); drawings_type.append("fill_between")
            
    self._postdrawing_settings(axes, legend, loc, labels, font_sizes, 
                         xlim, ylim,xpadding,ypadding,axis_style,X,Y)
    return drawing


def step(self, X = [],Y = [],  # X-Y points in the graph.
        labels = [], legend = [],       # Basic Labelling
        color = None,  lw = 2, alpha = 1.0,  # Basic line properties
        nf = 0, na = 0,          # New axis. To plot in a new axis         # TODO: shareX option
        ax = None, position = [], projection = "2d", # Type of plot
        sharex = None, sharey = None,
        fontsize = 20,fontsizeL = 10, fontsizeA = 15,  # The font for the labels in the axis
        xlim = None, ylim = None, xlimPad = None, ylimPad = None, # Limits of vision
        ws = None, Ninit = 0,     
        loc = "best",    
        dataTransform = None,
        xaxis_mode = None,yaxis_mode = None,AxesStyle = None,   # Automatically do some formatting :)
        marker = [" ", None, None],
        where = "pre", # pre post mid ## TODO, part of the step. How thw shit is done
        fill = 0,
        fill_offset = 0, 
        ):         

    # Management of the figure and properties
    ax = self.figure_management(nf, na, ax = ax, sharex = sharex, sharey = sharey,
                      projection = projection, position = position)
    ## Preprocess the data given so that it meets the right format
    X, Y = self.preprocess_data(X,Y,dataTransform)
    NpY, NcY = Y.shape
    plots,plots_typ =  self.init_WidgetData(ws)

    ##################################################################
    ############### CALL PLOTTING FUNCTION ###########################
    ##################################################################
    ## TODO. Second case where NcY = NcX !!

    if (Y.size != 0):  # This would be just to create the axes
    ############### CALL PLOTTING FUNCTION ###########################
        for i in range(NcY):  # We plot once for every line to plot
            self.zorder = self.zorder + 1  # Setting the properties
            colorFinal = self.get_color(color)
            legend_i = None if i >= len(legend) else legend[i]
            alpha_line = alpha if fill == 0 else 1
            plot_i, = ax.step(X[self.start_indx:self.end_indx],Y[self.start_indx:self.end_indx:,i], 
                     lw = lw, alpha = alpha_line, color = colorFinal,
                     label = legend_i, zorder = self.zorder,
                     where = where)
            plots.append(plot_i)
            plots_typ.append("plot")
            # Filling if needed
            if (fill == 1):  
                XX,YY1, YY2 = ul.get_stepValues(X[self.start_indx:self.end_indx],Y[self.start_indx:self.end_indx:,i], y2 = 0, step_where = where)
                self.fill_between(x = XX,
                                  y1 = YY1,
                                    y2 = fill_offset, color = colorFinal,alpha = alpha,
                                    step_where = where)


    ############### Last setting functions ###########################
    self.store_WidgetData(plots_typ, plots)     # Store pointers to variables for interaction
    
    self.update_legend(legend,NcY,ax = ax, loc = loc)    # Update the legend 
    self.set_labels(labels)
    self.set_zoom(ax = ax, xlim = xlim,ylim = ylim, xlimPad = xlimPad,ylimPad = ylimPad)
    self.format_xaxis(ax = ax, xaxis_mode = xaxis_mode)
    self.format_yaxis(ax = ax, yaxis_mode = yaxis_mode)
    self.apply_style(nf,na,AxesStyle)
    
    return ax

def plot_filled(self, X = [],Y = []):
    x = X[self.start_indx:self.end_indx]
    ############### CALL PLOTTING FUNCTION ###########################
    for i in range(0,NcY):  # We plot once for every line to plot

        if (fill_mode ==  "stacked"):
#            print "FFFFFFFFFFFFFFFFFFFFFFF"
            if (i == 0):   # i  for i in range(NcY)
                y1 = Y[self.start_indx:self.end_indx,i]
                y2 = 0 
            else:
                y2 = y1 
                y1 = y2 + Y[self.start_indx:self.end_indx,i]
                
        elif(fill_mode ==  "between"):
                y2 = Y[self.start_indx:self.end_indx,i-1]
                y1 = Y[self.start_indx:self.end_indx,i]
        else:
            if (i == NcY -1):
                break;
            y2 = Y[self.start_indx:self.end_indx,i]
            y1 = Y[self.start_indx:self.end_indx,i+1]
        
        self.zorder = self.zorder + 1  # Setting the properties
        colorFinal = self.get_color(color)
        legend_i = None if i >= len(legend) else legend[i]
        # With this we add the legend ?
#        plot_i, = ax.plot([X[0],X[0]],[y1[0],y1[0]], lw = lw, alpha = alpha, 
#                 color = colorFinal, zorder = self.zorder)
        
        if (step_mode == "yes"):
            XX,YY1, YY2 = ul.get_stepValues(x,y1, y2, step_where = where)
            fill_i = self.fill_between(x = XX,
                              y1 = YY1,
                                y2 = YY2, color = colorFinal,alpha = alpha,
                                step_where = where)
        else:
            fill_i = self.fill_between(x = x,y1 = y1 ,y2 = y2, color = colorFinal,alpha = alpha, legend = [legend_i])
        

def bar(self, X = [],Y = [],  # X-Y points in the graph.
        labels = [], legend = [],       # Basic Labelling
        color = None,  lw = 2, alpha = 1.0,  # Basic line properties
        nf = 0, na = 0,          # New axis. To plot in a new axis         # TODO: shareX option
        ax = None, position = [], projection = "2d", # Type of plot
        sharex = None, sharey = None,
        fontsize = 20,fontsizeL = 10, fontsizeA = 15,  # The font for the labels in the axis
        xlim = None, ylim = None, xlimPad = None, ylimPad = None, # Limits of vision
        ws = None, Ninit = 0,     
        loc = "best",    
        dataTransform = None,
        xaxis_mode = None,yaxis_mode = None,AxesStyle = None,   # Automatically do some formatting :)
        marker = [" ", None, None],
        fill_mode =  "independent", # "between", "stacked","independent"
        # Particular pararm
        orientation = "vertical",
        barwidth = None,      # Rectangle width
        bottom = None,    ## If the y-axis start somewhere else
        despx = 0,      # Displacement in the x axis, it is done for the dates
                        # so that we can move some other things (Velero graph)
        align = "edge"  #  "center"   
       ):         

    # Management of the figure and properties
    ax = self.figure_management(nf, na, ax = ax, sharex = sharex, sharey = sharey,
                      projection = projection, position = position)
    ## Preprocess the data given so that it meets the right format
    X, Y = self.preprocess_data(X,Y,dataTransform)
    NpY, NcY = Y.shape
    plots,plots_typ =  self.init_WidgetData(ws)
    
#    print (X)
    ## We asume that X and Y have the same dimensions
#    print (self.formatXaxis)
    if (self.formatXaxis == "dates" or self.formatXaxis == "intraday"):
        X = ul.preprocess_dates(X)
        print ("Formating bar X to dates")
    if (type(barwidth) == type(None)):
        barwidth = self.get_barwidth(X, barwidth) * 0.8

#    print ("Barwidth: ", barwidth)
    if (Y.size != 0):  # This would be just to create the axes
    ############### CALL PLOTTING FUNCTION ###########################
        for i in range(NcY):  # We plot once for every line to plot
            self.zorder = self.zorder + 1  # Setting the properties
            colorFinal = self.get_color(color)
            legend_i = None if i >= len(legend) else legend[i]
            if(type(bottom) != type(None)):
                bottom = bottom[self.start_indx:self.end_indx].flatten()
            if (orientation == "vertical"):
                plot_i  = self.axes.bar(X[self.start_indx:self.end_indx].flatten(), Y[self.start_indx:self.end_indx:,i].flatten(), 
                            width = barwidth, align=align,
                              facecolor= colorFinal,alpha=alpha,
                              label = legend_i, zorder = self.zorder,
                              bottom = bottom)
            else:  # horixontal
                plot_i  = self.axes.bar(width = Y[self.start_indx:self.end_indx:,i].flatten(), 
                              height = barwidth, align=align,
                              facecolor= colorFinal,alpha=alpha,
                              label = legend_i, zorder = self.zorder,
                              left = bottom,
                              bottom = X[self.start_indx:self.end_indx].flatten(),
                             orientation = "horizontal")
            plots.append(plot_i)
            plots_typ.append("plot")

    ############### Last setting functions ###########################
    self.store_WidgetData(plots_typ, plots)     # Store pointers to variables for interaction
    
    self.update_legend(legend,NcY,ax = ax, loc = loc)    # Update the legend 
    self.set_labels(labels)
    self.set_zoom(ax = ax, xlim = xlim,ylim = ylim, xlimPad = xlimPad,ylimPad = ylimPad)
    self.format_xaxis(ax = ax, xaxis_mode = xaxis_mode)
    self.format_yaxis(ax = ax, yaxis_mode = yaxis_mode)
    self.apply_style(nf,na,AxesStyle)
    return ax
    