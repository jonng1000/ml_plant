# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:14:38 2021

@author: weixiong001

Explore features produced for ml
"""


import pandas as pd

FILE = 'reg_nwt_centrality_features.txt'
FILE2 = 'ath_ttr_clusters.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

'''
df
Out[54]: 
           ttr_deg_cen   ttr_bet_cen
Genes                               
AT1G01010     0.000568  3.570885e-08
AT1G20910     0.096524  8.316378e-03
AT1G33240     0.173175  2.576338e-02
AT1G75240     0.192732  1.842667e-02
AT1G76890     0.104410  8.571950e-03
               ...           ...
AT5G67550     0.001136  1.585849e-07
AT5G67560     0.000946  4.573353e-07
AT5G67590     0.000063  0.000000e+00
AT5G67600     0.001956  7.767142e-07
AT5G67630     0.002082  1.038512e-06

[15852 rows x 2 columns]

# Eyeball this in notepad+, various numbers seen in cluster_size
df2
Out[55]: 
           ttr_cluster_size  ...  ttr_cluster_id_54
Gene                         ...                   
AT1G01040              2372  ...                  0
AT1G51700              2372  ...                  0
AT1G64620              2372  ...                  0
AT2G28810              2372  ...                  0
AT2G37590              2372  ...                  0
                    ...  ...                ...
AT3G10580                 3  ...                  0
AT1G78650                 3  ...                  0
AT2G17580                 3  ...                  0
AT3G20770                 2  ...                  1
AT2G20710                 2  ...                  1

[15851 rows x 55 columns]
'''

