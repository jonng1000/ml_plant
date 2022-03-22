# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Calculates degree and inbetweeness centrality measures from a graph, and 
saves it to a file. Modified from ceontrality_nx.py
"""
import pandas as pd
import networkx as nx
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

FILE = 'ath_ppi.graphml'
OUTPUT = 'centrality_features.txt'

G = nx.read_graphml(FILE)
'''
>>> G.number_of_nodes()
10585
>>> G.number_of_edges()
50429
'''

deg_cen = nx.degree_centrality(G)
'''
# This is just fyi, for data exploration, not strictly necessary
max_dc = max(deg_cen.values())
mdc_genes = []
for k, v in deg_cen.items():
    if v == max_dc:
        mdc_genes.append(k)
'''
# At 100% of nodes, takes 13 min 41s
# At 10% of nodes, takes 1 min 20s
# At 1% of nodes, takes 10s
print('start', get_time())
bet_cen = nx.betweenness_centrality(G)
print('end', get_time())
'''
# This is just fyi, for data exploration, not strictly necessary
max(bet_cen.values())
Out[22]: 0.27645820561339834
[k for k, v in bet_cen.items() if v == max(bet_cen.values())]
Out[29]: ['AT5G03240']
'''

dc_df = pd.DataFrame.from_dict(deg_cen, orient='index')
dc_df.rename(columns={0: 'ppi_deg_cen'}, inplace=True)
bc_df = pd.DataFrame.from_dict(bet_cen, orient='index')
bc_df.rename(columns={0: 'ppi_bet_cen'}, inplace=True)

cen_df = pd.concat([dc_df, bc_df], axis=1)
cen_df.index.name = 'Genes'
'''
# No nan exists
cen_df.isnull().values.any()
Out[4]: False
'''
cen_df.to_csv(OUTPUT, sep='\t')

