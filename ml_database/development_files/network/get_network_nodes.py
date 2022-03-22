# -*- coding: utf-8 -*-
"""
Spyder Editor

From network in .graphml format. takes in the selected node and produces
the local neighbour, in the cytoscape json format
"""

import networkx as nx

FILE = 'overall_sk2.graphml'

# Read in the file
G = nx.read_graphml(FILE)
G2 = G.to_undirected()
# Preliminary data preprocessing
nodes_view = G2.nodes()
mapping_dict = {node:G2.nodes[node]['shared name'] for node in nodes_view}
H = nx.relabel_nodes(G2, mapping_dict)

# Function which produces local neighbourhood in cytoscape json format
def get_neighbours(node_name, new_graph):
    # Get local neighbourhood
    neighbours = new_graph.adj[node_name]
    adj_nodes = [x for x in neighbours]
    adj_nodes.append(node_name)
    # Processes neighbourhood into cytoscape json format
    local_graph = new_graph.subgraph(adj_nodes).copy()
    local_cyto = nx.cytoscape_data(local_graph)
    return local_cyto

# This is just to test, please comment out and write appropriate code to use
# this function's output, in production
neigh_cyto = get_neighbours('go_GO:0009808', H)
