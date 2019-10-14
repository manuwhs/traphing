
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#####  BUILDING FUNCTIONS #####

def subplots_adjust(self, left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0, hide_xaxis = True):
    # Adjusting the properties of the subplots
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    if (hide_xaxis):
        all_axes = self.get_axes()
        for i in range(len(all_axes)-1):
            axes = all_axes[i]
            self.hide_xaxis(axes)
            self.set_labels(axes, title = "", xlabel = "")
            

def subplot2grid(self, *args, **kwargs): #divisions, selection):
    
    """
    Same as the original :) ! But we put the new axis into the array
    # It creates an axes with the desired dimensions by dividing 
    # the axes in "divisions" and then subselecting the desired ones.
    if (self.fig == None):       # If there is no figure
        self.init_figure()
    """
    
    axes = plt.subplot2grid(*args,**kwargs)
    self._add_axes(axes)
    return axes
    
#######################################################################
############## Legacy land ############################################
#######################################################################
# TODO: Think if it is worth refactoring functionality.
    
def set_subplots(self, nr, nc, projection = "2d", sharex=False):
    """
    State a subplot partitition of a new figure.
    nr is the number of rows of the partition
    nc is the numbel of columns
    """
    self.init_figure()

    
    self.sharex_aux = sharex
    self.subplotting = 1  
    # Variable that indicates that we are subplotting
    # So when nf = 1, if this variable is 0, then 
    # we do not create a new figure but we paint in a
    # different window 
    
    self.nc = nc
    self.nr = nr
    
    
    if (self.subplotting_mode == 1):
        # Using gridspec library
        self.G = gridspec.GridSpec(nr, nc)
        
    elif(self.subplotting_mode == 0):
        ax = plt.subplot2grid((nr,nc),(0, 0))
        
    self.nci = 0
    self.nri = 0

    self.first_subplot = 1

def next_subplot(self, projection = "2d", sharex = None, sharey = None):
    # Moves to the next subpot to plot.
    # We move from left to right and up down.

    if (self.first_subplot == 1): # If it is the first plot
        # then we do not set the new subplot due to nf = 1
        # This way all the subplottings are the same
        # Select first plot.
        self.first_subplot = 0
    else:
        self.nci = (self.nci + 1) % self.nc
        if (self.nci == 0): # If we started new row
            self.nri = (self.nri + 1) % self.nr
            
        if (self.nri == (self.nr-1) and self.nci == (self.nc-1)): # If we are in the last graph 
            self.subplotting = 0

    if (self.subplotting_mode == 1):
        if (projection == "2d"):
            ax = plt.subplot(self.G[self.nri, self.nci], sharex = sharex, sharey = sharey )
        elif(projection == "3d"):
            ax = plt.subplot(self.G[self.nri, self.nci], projection='3d',  sharex = sharex, sharey = sharey  )
        elif (projection == "polar"):
            ax = plt.subplot(self.G[self.nri, self.nci],projection='polar',  sharex = sharex, sharey = sharey )
        
#        ax = plt.axes(position = position )
        # YEAH !!! Fucking axes does not work !!
#            position = ax.get_position()
#            ax.axis('off')
##            print position
#            ax = self.fig.add_axes(position, projection = projection)
            print ("subplot")
            
    elif(self.subplotting_mode == 0):
        if (projection == "2d"):
            ax = plt.subplot2grid((self.nr,self.nc),(self.nri, self.nci), sharex = sharex , sharey = sharey )
        elif(projection == "3d"):
            ax = plt.subplot2grid((self.nr,self.nc),(self.nri, self.nci), projection='3d', sharex = sharex , sharey = sharey )
        elif(projection == "polar"):
            ax = plt.subplot2grid((self.nr,self.nc),(self.nri, self.nci), projection= 'polar', sharex = sharex , sharey = sharey )
            print ("subplot2grid")
    if (self.nci + self.nri == 0):
        plt.tight_layout()  # So that the layout is tight

    self.axes = ax
    self.axes_list.append(ax)
    
    return ax
    
    