import matplotlib.pyplot as plt
from .. import utils as ul
from .trapyngColors import cd

def _init_variables(self, w = 20, h = 12, lw = 2):
        """ Initialize all the internal variables to do all the cool stuff later.
        It handles the intuitive logic later
        """
        self.w = w;    # X-width
        self.h = h;    # Y-height
        self.lw = lw   # line width
        
        self.prev_fig = []  # List that contains the previous plot.
        # When a new figure is done, we put the current one here and
        # create a new variable. Silly way to do it though
        
        self.figure = None
        self.axes = None
        
        self.nplots = 0;  # Number of plots
        self.labels = []  # Labels for the plots
        self.plot_y = []  # Vectors of values to plot x-axis
        self.plot_x = []  # Vectors of values to plot y-axis
        
        # Set of nice colors to iterate over when we do not specify color

#        self.colors = ["k","b", "g", "r", "c", "m","y"] 
        self.colors = [cd["dark navy blue"],cd["golden rod"],
                       cd["blood"], cd["chocolate"],  cd["cobalt blue"],
                 cd["cement"], cd["amber"], cd["dark olive green"]]
        
        self.colorIndex = 0;  # Index of the color we are using.
        self.X = ul.fnp([])
        self.legend = []
        
        self.subplotting_mode = 1 # Which functions to use for subplotting
        self.subplotting = 0;  # In the beggining we are not subplotting
        self.ticklabels = []   # To save the ticklabels in case we have str in X
        
        self.Xticklabels = []  # For 3D
        self.Yticklabels = []
        self.zorder = 1   # Zorder for plotting
        
        ## Store enough data to redraw and reference the plots for the interactivity
        self.plots_list = []; # List of the plots elements, 
        self.plots_type = []; # Type of plot of every subplot
        
        self.axes_list = []   # We store the list of indexes
        self.Data_list = []  # We need to store a pointer of the data in the graph
        self.widget_list = []  # We need to store reference to widget so that
        self.num_hidders = 0


def _figure_management(self, axes = None, sharex = None, sharey = None, 
                      position = [], projection = "2d"):
    """
    This function is suposed to deal with everything that has to do with initializating figure, axis, subplots...
    """
    if(self.figure is None):
        self.init_figure()
    axes = self._manage_axes(axes = axes, sharex = sharex, sharey = sharey,
                             position = position, projection = projection)
    return axes

def init_figure(self,w = 20, h = 12, lw = 2):
        self._init_variables()
        self.figure = plt.figure()  
        return self.figure
    
def close_figure(self,  *args, **kwargs):
    return  plt.close( *args, **kwargs)
    

def save_figure(self,file_dir = "./image.png", bbox_inches = 'tight',
            size_inches = [],  close = False, dpi = 100):
    """ Function to save the current figure in the desired format
    Important !! Both dpi and sizeInches affect the number of pixels of the image
    - dpi: It is just for quality, same graph but more quality.
    - size_inches: The size in inches as a list You change the proportions of the window. The fontsize and 
    - thickness of lines is the same. So as the graph grows, they look smaller.
    """
    try:
        folders = file_dir.split("/")
        folders.pop(-1)
        path = "/".join(folders)
        ul.create_folder_if_needed(path);
    except:
        pass

    Winches, Hinches = self.figure.get_size_inches()  
    if (len(size_inches) > 0):
        self.figure.set_size_inches( (size_inches[0], size_inches[1]) )
        
    self.figure.savefig(file_dir,bbox_inches = bbox_inches, dpi = dpi )

    if (close == True):
        plt.close()
    else:
        # Transform back to keep displaying it
        self.figure.set_size_inches((Winches, Hinches) )  
    
#    gl.savefig('foodpi50.png', bbox_inches='tight',  dpi = 50)
#    gl.savefig('foodpi100.png', bbox_inches='tight',  dpi = 100)
#    gl.savefig('foodpi150.png', bbox_inches='tight',  dpi = 150)
#
#    gl.savefig('foosize1.png', bbox_inches='tight',  sizeInches = [3,4])
#    gl.savefig('foosize2.png', bbox_inches='tight',  sizeInches = [6,8])
#    gl.savefig('foosize3.png', bbox_inches='tight',  sizeInches = [8,11])
#    gl.savefig('foosize4.png', bbox_inches='tight',  sizeInches = [10,14])


