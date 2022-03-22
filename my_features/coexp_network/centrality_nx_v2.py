# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Calculates degree and inbetweeness centrality measures from a graph, and 
saves it to a file. Modified from centrality_nx.py in
D:\GoogleDrive\machine_learning\my_features\ppi_network

Total time is about 3h 10min, need to figure out how to parallelise
this
"""
import pandas as pd
import networkx as nx
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


FILE = 'ath_coe.graphml'
OUTPUT = 'ath_coe_centrality_features.txt'
# Used to label features with unique identifiers
SUFFIX = 'coe'

print('start', get_time())
G = nx.read_graphml(FILE)

deg_cen = nx.degree_centrality(G)
bet_cen = nx.betweenness_centrality(G)

dc_df = pd.DataFrame.from_dict(deg_cen, orient='index')
dc_df.rename(columns={0: SUFFIX + '_deg_cen'}, inplace=True)
bc_df = pd.DataFrame.from_dict(bet_cen, orient='index')
bc_df.rename(columns={0: SUFFIX + '_bet_cen'}, inplace=True)

cen_df = pd.concat([dc_df, bc_df], axis=1)
cen_df.index.name = 'Genes'
'''
# No nan exists
cen_df.isnull().values.any()
Out[4]: False
'''
cen_df.to_csv(OUTPUT, sep='\t')
print('end', get_time())

