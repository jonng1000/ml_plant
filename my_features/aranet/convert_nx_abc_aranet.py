# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Converts network into 
graphml format for downstream analysis, and the abc format for mcl
"""

import pandas as pd
import networkx as nx

FILE = 'AraNet.txt'
OUTPUT = 'aranet.graphml'
ABC_OUTPUT = 'aranet.abc'

df = pd.read_csv(FILE, header=None, sep='\t')
df = df.rename(columns={0: 'source', 1: 'target', 2:'log likelihood score'})
G = nx.from_pandas_edgelist(df, 'source', 'target', 'log likelihood score')

'''
>>> G.number_of_nodes()
22894
>>> G.number_of_edges()
895000
'''
# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)
# Converts to abc format for mcl
df.to_csv(ABC_OUTPUT, header=False, index=False, sep=' ')