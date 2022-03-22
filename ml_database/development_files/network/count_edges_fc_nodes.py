# -*- coding: utf-8 -*-
"""
Spyder Editor

For each node, calculate the number of unique feature categories which it is
connected to.
"""

import networkx as nx
import pandas as pd

FILE = 'overall_sk2.graphml'
OUTPUT= 'num_categories_nodes.txt'

# Read in the file
G = nx.read_graphml(FILE)
G2 = G.to_undirected()
# Preliminary data preprocessing
nodes_view = G2.nodes()
mapping_dict = {node:G2.nodes[node]['shared name'] for node in nodes_view}
H = nx.relabel_nodes(G2, mapping_dict)

node_category = {}
for node in H.nodes():
    feat_category = H.nodes[node]['feat_category']
    set_category = set()    
    neighbours = H.adj[node]
    for one in neighbours:
        feat_cat = H.nodes[one]['feat_category']
        set_category.add(feat_cat)
    num_categories = len(set_category)
    
    if node in node_category:
        print('Error! node is already present')
    node_category[node] = num_categories

node_category_df = pd.DataFrame.from_dict(node_category, orient='index')
node_category_df.rename(columns={0: 'num_categories_w_edges'}, inplace=True)
sorted_df = node_category_df.sort_values(by=['num_categories_w_edges'], ascending=False)
sorted_df.index.name = 'nodes'

sorted_df.to_csv(OUTPUT, sep='\t')