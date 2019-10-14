from collections import OrderedDict

def _update_legend(self, axes, n_drawings, legend = [], loc = "best"):
    # TODO: make something so that the legends do not overlap when we have shared axes.
    
    if type(legend) == type([]):
        if(len(legend) > 0):
            self.legend.extend(legend)
        else:
            self.legend.extend(["Line"]*n_drawings)
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


def _set_font_size_list_inputs(self, axes, list_font_sizes = None):
    """
    Just a helper function for the other one
    """
    if list_font_sizes is not None:
        while(len(list_font_sizes) < 6):
            list_font_sizes.append(None)
        self.set_font_sizes(axes, list_font_sizes[0], list_font_sizes[1], list_font_sizes[2],
                       list_font_sizes[3],list_font_sizes[4],list_font_sizes[5])
        
def set_font_sizes(self, axes = None, title = None, xlabel = None, ylabel = None, 
                  legend = None, xticks = None, yticks = None):
                      
    if (type(axes) == type(list())):
        for ax_i in axes:
            self.set_font_sizes(axes = ax_i, title = title, xlabel = xlabel, ylabel = ylabel, 
                  legend = legend, xticks = xticks, yticks = yticks)
    else:
        # Set fontsize of the tittle
        if title is not None:
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

            
def _set_labels_list_input(self, axes, list_labels = ["title","x_label","y_label"]):
    """
    Just a helper function for the other one
    """
    if list_labels is not None:
        while(len(list_labels) < 4):
            list_labels.append(None)
        self.set_labels(axes, list_labels[0], list_labels[1], list_labels[2],
                       list_labels[3])


def set_labels(self, axes = None, title = None, xlabel = None, ylabel = None,  subtitle = None):
    if title is not None:
#        ax.title.set_text(title)
#        ax.title(title, y=1.01)
        axes.set_title(title, pad = 20)
    if xlabel is not None:
        axes.set_xlabel(xlabel)
    if ylabel is not None:
        axes.set_ylabel(ylabel)
        
        
def add_text(self, axes, x,y, text = r'an equation: $E=mc^2$',fontsize = 15):
    return axes.text(x, y, text, fontsize=fontsize)

## TODO: Refactor code
def format_legend_2():

    ## Format the legend !!
    maLeg = ax1.legend(loc=9, ncol=2, prop={'size':7},
               fancybox=True, borderaxespad=0.)
    maLeg.get_frame().set_alpha(0.4)
    textEd = ax1.get_legend().get_texts()
    pylab.setp(textEd[0:5], color = 'w')
        
    ## Remove the xticklabels of the other axes !!
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    ## Final touches !!! 
    plt.suptitle("Trasing Station",color='k', fontsize = 20)


