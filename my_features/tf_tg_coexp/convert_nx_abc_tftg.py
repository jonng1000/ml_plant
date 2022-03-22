# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Converts network into 
graphml format for downstream analysis, and the abc format for mcl
"""

import pandas as pd
import networkx as nx

FILE = 'tf_tg_network.txt'
OUTPUT = 'tftg_reg_net.graphml'
ABC_OUTPUT = 'tftg_reg_net.abc'

df = pd.read_csv(FILE, sep='\t')

G = nx.from_pandas_edgelist(df, 'AGI',
                            'AGI_for_TFs')

'''
>>> G.number_of_nodes()
15852
>>> G.number_of_edges()
280406
'''
# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)
# Converts to abc format for mcl
df.to_csv(ABC_OUTPUT, header=False, index=False, sep=' ')
'''
# Just for tests
test = df.iloc[:10, :10]
GT = nx.from_pandas_edgelist(test, 'AGI','AGI_for_TFs')
nx.write_graphml_lxml(GT, 'tftg_test.graphml')
GT1 = nx.from_pandas_edgelist(test, 'AGI', 'AGI_for_TFs', create_using=nx.DiGraph())
nx.write_graphml_lxml(GT1, 'tftg_test1.graphml')
test.to_csv('tftg_test.txt', sep='\t') # later this has directed added

GD = nx.from_pandas_edgelist(df, 'AGI', 'AGI_for_TFs', create_using=nx.DiGraph())
nx.write_graphml_lxml(GD, 'tftg_reg_net1.graphml')
'''