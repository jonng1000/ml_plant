# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Calculates degree and inbetweeness centrality measures from a graph, and 
saves it to a file
"""
import pandas as pd
import networkx as nx
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

FILE = 'aranet.graphml'
OUTPUT = 'aranet_centrality_features.txt'

G = nx.read_graphml(FILE)
'''
>>> G.number_of_nodes()
22894
>>> G.number_of_edges()
895000
'''
# This is calculated instantaneously
deg_cen = nx.degree_centrality(G)

# Takes about 4.5 h
print('start', get_time())
bet_cen = nx.betweenness_centrality(G)
print('end', get_time())


# This section needs to change as its dataset dependent
dc_df = pd.DataFrame.from_dict(deg_cen, orient='index')
dc_df.rename(columns={0: 'agn_deg_cen'}, inplace=True)
bc_df = pd.DataFrame.from_dict(bet_cen, orient='index')
bc_df.rename(columns={0: 'agn_bet_cen'}, inplace=True)
cen_df = pd.concat([dc_df, bc_df], axis=1)
cen_df.index.name = 'Genes'

'''
# No nan exists
cen_df.isnull().values.any()
Out[4]: False
'''
cen_df.to_csv(OUTPUT, sep='\t')

