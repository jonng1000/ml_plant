# -*y- coding: utf-8 -*-
"""
Created on 230620

@author: weixiong

Loads and explore graph saved from cytoscape, doesn't work tho, as cytoscape
doesnt seem to create the correct graph.
"""

import pandas as pd
import networkx as nx

FILE = 'BIOGRID-ORGANISM-Arabidopsis_thaliana_Columbia-4.0.189.tab3.txt.graphml'
G = nx.read_graphml(FILE)
'''
FILE = 'BIOGRID-ALL-4.0.189.tab3.txt'

df = pd.read_csv(FILE, sep='\t')

m1 = df['Organism Name Interactor A'].str.contains('Arabidopsis', regex=False)
m2 = df['Organism Name Interactor B'].str.contains('Arabidopsis', regex=False)
'''
'''
>>> df.loc[:,'Experimental System Type']
0          physical
1          physical
2          physical
3          physical
4          physical
             ...
1868156    physical
1868157    physical
1868158    physical
1868159    physical
1868160    physical
Name: Experimental System Type, Length: 1868161, dtype: object
>>> df.loc[:,'Experimental System Type'].unique()
array(['physical', 'genetic'], dtype=object)
'''

#ydropped_df.to_csv(OUTPUT, sep='\t')

