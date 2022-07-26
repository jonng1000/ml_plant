# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:49:11 2021

@author: weixiong001

Get number of nodes and edges from network, based on various thresholds, which
are top X% of edges in the network.
"""


import pandas as pd

FILE = 'nonzero_mr.txt'
OUTPUT = 'network_thresholds.txt'


df = pd.read_csv(FILE, sep='\t', index_col=0)
sorted_df = df.sort_values(by=['MR'])

partial = [one/100 for one in range(10,101,10)]
lst_cutoff = [0.01, 0.05, 0.07] + partial

master_lst = []
for i in lst_cutoff:
    edges = round(len(sorted_df)*i)
    top = sorted_df[:edges]
    node_names = set(top['f1']) | set(top['f2'])
    nodes = len(node_names)
    cutoff = int(i*100)
    temp = [cutoff, nodes, edges]
    master_lst.append(temp)

network_df = pd.DataFrame (master_lst, columns=['threshold (%)', 'nodes', 'edges'])
network_df.index.name = 'id'

network_df.to_csv(OUTPUT, sep='\t')