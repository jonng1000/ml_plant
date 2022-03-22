# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 19:49:38 2022

@author: weixiong001
"""

from goatools import obo_parser
import networkx as nx

FILE = '../development_files/network/overall_sk2.graphml'
GO_OBO = 'go.obo'
GO_ID = 'GO:0019748'  # Secondary metabolic process

# Read in files
G = nx.read_graphml(FILE)
go = obo_parser.GODag(GO_OBO)
# Processes GO file
go_term = go[GO_ID]
children = go_term.get_all_children()
print(len(children), type(children))
list_children = list(children)
list_children.append(GO_ID)  # parent term is not added by default

# Processing of graph
G2 = G.to_undirected()
nodes_view = G2.nodes()
mapping_dict = {node:G2.nodes[node]['shared name'] for node in nodes_view}
H = nx.relabel_nodes(G2, mapping_dict)

nodes_set = {x.replace('go_GO', 'GO') if x.startswith('go_GO') else x for x in H.nodes()}

sec_GO_network = nodes_set & set(list_children)
