# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:14:38 2021

@author: weixiong001

Explore features produced for ml
"""


import pandas as pd

FILE = 'ath_centrality_features.txt'
FILE2 = 'ath_ppi_clusters.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

'''
df
Out[38]: 
           ppi_deg_cen  ppi_bet_cen
Genes                              
AT4G00020     0.000378     0.000007
AT5G20850     0.000567     0.000019
AT3G22880     0.000756     0.000351
AT5G61380     0.004441     0.001748
AT2G43010     0.001890     0.000482
               ...          ...
AT2G46150     0.000094     0.000000
AT3G59400     0.000094     0.000000
AT4G12280     0.000094     0.000000
AT5G52310     0.000094     0.000000
AT5G58787     0.000094     0.000000

[10585 rows x 2 columns]

# Eyeball this in notepad+, various numbers seen in cluster_size
df2
Out[39]: 
           ppi_cluster_size  ...  pid_cluster_id_1294
Gene                         ...                     
AT5G24930               917  ...                    0
AT4G25500               917  ...                    0
AT2G21660               917  ...                    0
AT2G39730               917  ...                    0
AT1G55490               917  ...                    0
                    ...  ...                  ...
AT1G54380                 2  ...                    0
AT2G20610                 2  ...                    0
AT5G37478                 2  ...                    0
AT2G25010                 2  ...                    1
AT4G13260                 2  ...                    1

[10352 rows x 1295 columns]
'''

