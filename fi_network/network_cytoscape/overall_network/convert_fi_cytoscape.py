# -*y- coding: utf-8 -*-
"""
Created on 011020
@author: weixiong

Creates feature importance network with additional node attributes, in .graphml format
"""

import pandas as pd
import networkx as nx

FILE = '../selected_mr.txt'
FILE2 = 'feat_cat_info_nofilter.txt'
OUTPUT = 'fi_w_info.graphml'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df = df.rename(columns={'f1': 'source', 'f2': 'target'})
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

'''
# This shows missing nodes from my two input files, due to the problem below
all_nodes = set(df['source']) | set(df['target'])
missing_rel_fc = set(df2.index) - all_nodes
missing_rel_g = all_nodes - set(df2.index)
'''
# This is needed as feature category info files was derived from mcl output,
# which cannot accept spaces in node names, so I have to replace spaces in my
# original df
df['source'] = df['source'].str.replace(' ','_')
df['target'] = df['target'].str.replace(' ','_')

G = nx.from_pandas_edgelist(df, 'source', 'target', 'invert_ranks')
node_attr = df2.to_dict('index')
nx.set_node_attributes(G, node_attr)
'''
# This is when an F1 and R sq score of 0.4 is used
G.number_of_nodes()
Out[205]: 1342

G.number_of_edges()
Out[206]: 5308
'''
# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)
