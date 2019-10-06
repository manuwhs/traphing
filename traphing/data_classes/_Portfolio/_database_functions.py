# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 03:04:26 2016

@author: montoya
"""

import pandas as pd
import numpy as np

import datetime as dt
import matplotlib.pyplot as plt
import copy as copy
import time as time

import datetime
import gc


## Operations from a list of symbols 
def load_data_from_csv(self,file_dir = "./storage/"):
    for symbol_name in self.symbol_names_list:
        self[symbol_name].load_data_from_csv(file_dir)
    
def add_data_from_csv(self,file_dir = "./storage/"):
    for symbol_name in self.symbol_names_list:
        self[symbol_name].add_data_from_csv(file_dir)

def save_to_csv(self,file_dir = "./storage/"):
    for symbol_name in self.symbol_names_list:
        self[save_to_csv].save_to_csv(file_dir)

def update_csv (self, storage_folder, updates_folder):
    # Function that loads from 2 different folders, joins the data and saves it back
    self.load_data_from_csv(storage_folder)
    self.add_data_from_csv(updates_folder)
    self.save_to_csv(storage_folder)
    

    