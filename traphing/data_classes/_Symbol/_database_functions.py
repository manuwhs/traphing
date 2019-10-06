# -*- coding: utf-8 -*-
import pandas as pd

#############################################################
################# BASIC FUNCTIONS FOR ALL time  ########
############################################################

def load_data_from_csv(self,file_dir = "./storage/"):
    for timeframe in self.timeframes_list:
        self[timeframe].load_data_from_csv(file_dir)
    
def add_data_from_csv(self,file_dir = "./storage/"):
    for timeframe in self.timeframes_list:
        self[timeframe].add_csv(file_dir)

def save_to_csv(self,file_dir = "./storage/"):
    for timeframe in self.timeframes_list:
        self[timeframe].save_to_csv(file_dir)

def update_csv (self, storage_folder, updates_folder):
    # Function that loads from 2 different folders, joins the data and saves it back
    self.load_data_from_csv(storage_folder)
    self.add_data_from_csv(updates_folder)
    self.save_to_csv(storage_folder)

"""
Functions related to the info
"""
def map_dict_to_objects(pandas_df, obj):
    ## TODO to utils and finish func
    ## This function takes a dictionary-like object and maps its fields with the ones in an object
    
    obj_attributes = []
    pandas_columns = []
    
    for key in pandas_columns:
        obj.set_attr(key, pandas_columns[key])
    
def set_symbol_info_from_df(self, df):
    # Symbol_name,PointSize,MinTickValue,ContractSize,Currency,PriceNow
    info = df.loc[df['symbol_name'] == self.symbol_name]
    map_dict_to_objects(info, self.properties)
