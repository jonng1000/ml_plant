# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:14:38 2021

@author: weixiong001

Explore features produced for ml
"""


import pandas as pd

FILE = 'aranet_centrality_features.txt'
FILE2 = 'ath_agn_clusters.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

'''
df
Out[109]: 
           agn_deg_cen  agn_bet_cen
Genes                              
AT2G33370     0.032543     0.000471
AT4G34555     0.031407     0.000502
AT1G04480     0.036955     0.000452
AT2G27530     0.033504     0.000456
AT4G16720     0.032674     0.000297
               ...          ...
AT5G57880     0.000044     0.000000
AT1G48580     0.000044     0.000000
AT1G65910     0.000044     0.000000
AT1G53100     0.000044     0.000000
AT2G04840     0.000044     0.000000

[22894 rows x 2 columns]

# Eyeball this in notepad+, various numbers seen in cluster_size
df2
Out[115]: 
           agn_cluster_size  ...  agi_cluster_id_2956
Gene                         ...                     
AT2G33370               493  ...                    0
AT4G34555               493  ...                    0
AT1G04480               493  ...                    0
AT2G27530               493  ...                    0
AT4G16720               493  ...                    0
                    ...  ...                  ...
AT4G18850                 2  ...                    0
AT2G02650                 2  ...                    0
AT3G25130                 2  ...                    0
AT1G72080                 2  ...                    1
AT2G20720                 2  ...                    1

[22568 rows x 2957 columns]
'''

