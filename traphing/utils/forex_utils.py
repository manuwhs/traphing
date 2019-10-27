#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:25:25 2019

@author: montoya
"""
import networkx as nx

import pandas as pd
import numpy as np

def reverse_forex_name(symbol_name):
    return symbol_name[3:] + symbol_name[:3]

def get_exchange_cycle(currencies, symbol_names_list = None):
    """ It returns a list with the forex conversions cycle
    """
    exchanges = []
    for i in range(len(currencies)):
        currency_from = currencies[i]
        currency_to = currencies[(i+1)%len(currencies)]
        
        exchange = currency_from + currency_to
        reverse_exchange = reverse_forex_name(exchange)
        if symbol_names_list is not None:
            if (exchange in symbol_names_list) | (reverse_exchange in symbol_names_list):
                exchanges.append(exchange)
            else:
                print("No direct exchange ",currency_from, currency_to)
                return None
        else: 
            exchanges.append(exchange)
    return exchanges

def get_exchange_symbol_names(currencies, symbol_names_list):
    """ It returns a list with the forex conversions cycle
    """
    exchanges = []
    for i in range(len(currencies)):
        currency_from = currencies[i]
        currency_to = currencies[(i+1)%len(currencies)]
        
        exchange = currency_from + currency_to
        reverse_exchange = reverse_forex_name(exchange)

        if (exchange in symbol_names_list):
            exchanges.append(exchange)
        elif (reverse_exchange in symbol_names_list):
            exchanges.append(reverse_exchange)
        else:
            print("No direct exchange ",currency_from, currency_to)
            return None
  
    return exchanges

"""
ADVANCED LEGACY
"""

def get_forex_graph(currencies, forex_dataframe: pd.DataFrame, timestamp):
    """It prints the negative cycle
    
    """
    nodes = currencies
    forex_exchanges = list(forex_dataframe.columns)
    

    edges = []
    for forex_exchange in forex_exchanges:
        currency_from = forex_exchange[:3]
        currency_to = forex_exchange[3:]
        exchange_rate = forex_dataframe.loc[timestamp][forex_exchange]
        
        if (currency_from in currencies) & (currency_to in currencies):
            edge_1  = (currency_from,currency_to,{'w':  np.log(exchange_rate)})
            edge_2  = (currency_to,currency_from,{'w':  np.log(1/exchange_rate)})
            
            edges.extend([edge_1,edge_2])
    
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def get_forex_cycles(G):
    cycles = nx.simple_cycles(G)
    weights = nx.get_edge_attributes(G, 'w')
    
    cycles_list = []
    gains_list = []
    for cycle in cycles:
            cycle.append(cycle[0])
            sumw = sum([weights[(cycle[i-1], cycle[i])] for i in range(1, len(cycle))])
            cycles_list.append(cycle)
            gains_list.append(np.exp(sumw))
    
    gains_list, cycles_list = (list(t) for t in zip(*sorted(zip(gains_list, cycles_list))))
    
#    for i in range(len(gains_list)):
#        print (cycles_list[i], " ", gains_list[i])
        
    return gains_list, cycles_list 

if(0):
    import forex_utils as fu
    gain_df = []
    for timestamp in indicators_df.index:
        G = fu.get_forex_graph(currencies_list, indicators_df, timestamp)
        gains_list, cycles_list  = fu.get_forex_cycles(G)
    #    print (cycles_list[0], " ", gains_list[0])
        gain_df.append(gains_list[0])
    
    gl.plot(indicators_df.index, gain_df)