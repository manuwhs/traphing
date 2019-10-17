import copy
import pandas as pd

import Coliseum_core as Coc
class Coliseum:
    """
    Class with functionalities to control all entry and exit strategies!
    It provides an interface between the brain and all the strategies.
    """
    def __init__(self, strategies_dict):
        self.entry_strategies_dict = strategies_dict 
        self.exit_strategies_dict = strategies_dict 
        
    def add_strategy():
    #######################################################################
    ############## DDBB methods ###########################################
    #######################################################################

    
    #######################################################################
    ############## CORE Methods ###########################################
    #######################################################################
    open_position = Coc.open_position
    get_position_indx = Coc.get_position_indx
    close_position = Coc.close_position
    add_position = Coc.add_position
    get_position_indx = Coc.get_position_indx
    close_position_by_indx = Coc.close_position_by_indx
    get_positions_symbol = Coc.get_positions_symbol
    
    update_prices = Coc.update_prices
    close_positions = Coc.close_positions
    
    set_date = Coc.set_date
    
    load_csv = Coc.load_csv
