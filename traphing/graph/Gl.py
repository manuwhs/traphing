from . import _figure 
from . import _axes 
from . import _advanced
from . import _3D 
from . import _setting
from . import _axis 
from . import _subplots
from . import _zoom 
from . import _plots
from . import _texts
from . import _data_preprocessing
from . import _dates_formatting
from .GUI import _GUI 

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class GraphicalLibraryFigure ():
    
    def __init__(self,w = 20, h = 12, lw = 2):
        self._init_variables(w = w, h = h, lw = lw)
    
    ####################### Figure functions  #######################
    _figure_management = _figure._figure_management
    _init_variables = _figure._init_variables

    init_figure = _figure.init_figure    
    save_figure = _figure.save_figure
    close_figure = _figure.close_figure

    ####################### Axis functions #######################
    format_axis = _axis.format_axis
    format_xaxis = _axis.format_xaxis
    format_yaxis = _axis.format_yaxis
    
    apply_axis_style = _axis.apply_axis_style
    set_xticks_rotation = _axis.set_xticks_rotation
    set_yticks_rotation = _axis.set_yticks_rotation
    
    color_axis = _axis.color_axis
    hide_xaxis =  _axis.hide_xaxis
    hide_yaxis =  _axis.hide_yaxis
    
    ####################### Setting functions #######################
    _predrawing_settings = _setting._predrawing_settings
    _postdrawing_settings = _setting._postdrawing_settings
    get_color = _setting.get_color
    
    ##################### Text functions ############################
    _update_legend = _texts._update_legend
    format_legend = _texts.format_legend
 
    set_font_sizes = _texts.set_font_sizes
    _set_font_size_list_inputs = _texts._set_font_size_list_inputs
    _set_labels_list_input = _texts._set_labels_list_input
    set_labels = _texts.set_labels
    add_text = _texts.add_text
    
    ######################## Axes functions #######################
    _add_axes = _axes._add_axes
    _manage_axes = _axes._manage_axes
    _twin_axes = _axes._twin_axes
    
    create_axes = _axes.create_axes
    get_axes = _axes.get_axes
    
    ####################### Zoom functions #########################
    set_xlim = _zoom.set_xlim
    set_ylim = _zoom.set_ylim
    set_zoom = _zoom.set_zoom
    set_ylim_padding = _zoom.set_ylim_padding
    set_xlim_padding = _zoom.set_xlim_padding

 
    ####################### Subplots functions #######################
    set_subplots = _subplots.set_subplots
    next_subplot = _subplots.next_subplot
    subplots_adjust =  _subplots.subplots_adjust
    subplot2grid = _subplots.subplot2grid

    #################### data preprocessing #########################
    _preprocess_data = _data_preprocessing._preprocess_data
    _get_barwidth = _data_preprocessing._get_barwidth
#    _dates_formatting = _data_preprocessing._dates_formatting
    
    ####################### Basic graph functions #######################
    plot = _plots.plot
    scatter = _plots.scatter
    stem = _plots.stem
    fill_between = _plots.fill_between
    bar = _plots.bar
    ####################### Widgets ######################################
    _init_WidgetData = _GUI._init_WidgetData
    

    ####################### Advanced  #######################
    barchart = _advanced.barchart
    candlestick = _advanced.candlestick
        
    if(0):
        ####################### 3D functions #######################
        preproces_data_3D = gr3D.preproces_data_3D
        format_axis_3D = gr3D.format_axis_3D
        plot_3D = gr3D.plot_3D
        bar_3D = gr3D.bar_3D
        scatter_3D = gr3D.scatter_3D
    
        ####################### Specific Math graphs #######################
        plot_timeRegression = grad.plot_timeRegression
        histogram = grad.histogram
        
        ####################### Widgets #######################
        add_slider = grGUI.add_slider
        add_hidebox = grGUI.add_hidebox
        plot_wid = grGUI.plot_wid
        add_selector = grGUI.add_selector
        add_onKeyPress = grGUI.add_onKeyPress
        store_WidgetData = grGUI.store_WidgetData
        init_WidgetData = grGUI.init_WidgetData
        

gl = GraphicalLibraryFigure()

