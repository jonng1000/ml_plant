# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:13:06 2020

@author: weixiong001

Converts HRR outout of coexpressed genes, into a coexpression graph, and saves
it in graphml format for downstream work.
"""

import csv
import pandas as pd
import networkx as nx

FILE = 'ARATH-matrix-HRR.txt'
OUTPUT = 'ath_coe.graphml'

master_lst = []
with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for row in csvreader:
        # HRR value is in row[3] 
        if int(row[3]) < 100:
            # This is one edge:
            # row[0] is gene A, row[1] is gene B,
            # row[2] is PCC
            one_edge = [row[0], row[1], row[2], row[3]]
            master_lst.append(one_edge)

df = pd.DataFrame(master_lst, columns = ['Gene_A', 'Gene_B', 'PCC', 'HRR'])
G = nx.from_pandas_edgelist(df, 'Gene_A', 'Gene_B', ['PCC', 'HRR'])

# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)

'''
Just for exploring
G.number_of_nodes()
Out[82]: 23394

G.number_of_edges()
Out[83]: 673931
'''