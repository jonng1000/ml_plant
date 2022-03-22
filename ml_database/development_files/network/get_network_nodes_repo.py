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
def get_neighbours(node_name, new_graph = H):
    # Get local neighbourhood
    neighbours = new_graph.adj[node_name]
    adj_nodes = [x for x in neighbours]
    adj_nodes.append(node_name)
    # Processes neighbourhood into cytoscape json format
    local_graph = new_graph.subgraph(adj_nodes).copy()
    local_cyto = nx.cytoscape_data(local_graph)
    nodes = local_cyto['elements']['nodes']
    edges = local_cyto['elements']['edges']
    modifiedNodes= []
    modifiedEgdes = []

    for i in nodes:
        edge = i["data"]
        modifiedNodes.append({ "data": {
                                "id": edge["value"], 
                                "label": edge["value"], 
                                "degree_layout":edge["degree_layout"], 
                                "feat_cluster_id": edge["feat_cluster_id"], 
                                "feat_cluster_size": edge["feat_cluster_size"],
                                "name": edge["name"],
                                "new_name": edge["new_name"],
                                "selected": edge["selected"],
                                "shared name": edge["shared name"],
                                "feat_category": edge["feat_category"]
                            }})

    for i in edges:
        edge = i["data"]
        modifiedEgdes.append({ "data": {"source": edge["source"], "target": edge["target"], "label":edge["name"], "interaction": edge["interaction"], "selected": edge["selected"]}})

    return modifiedNodes, modifiedEgdes


neigh_cyto = get_neighbours('go_GO:0009808', H)
