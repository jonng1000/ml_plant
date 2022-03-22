# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Converts network into 
graphml format for downstream analysis, and the abc format for mcl

For feature imporance clusters
"""

import pandas as pd
import networkx as nx

FILE = 'selected_mr.txt'
OUTPUT = 'fi.graphml'
ABC_OUTPUT = 'fi.abc'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df = df.rename(columns={'f1': 'source', 'f2': 'target'})
G = nx.from_pandas_edgelist(df, 'source', 'target', 'invert_ranks')

'''
# This is when an F1 and R sq score of 0.7 is used
G.number_of_nodes()
Out[205]: 1318

G.number_of_edges()
Out[206]: 5128

# The above number of edges also corresponds to the number of rows in the .abc
# file
'''
# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)
# Converts to abc format for mcl
dropped = df.drop(columns=['MR'])
dropped['source'] = dropped['source'].str.replace(' ','_')
dropped['target'] = dropped['target'].str.replace(' ','_')
dropped.to_csv(ABC_OUTPUT, header=False, index=False, sep=' ')
