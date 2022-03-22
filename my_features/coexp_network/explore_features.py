# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:14:38 2021

@author: weixiong001

Explore features produced for ml
"""


import pandas as pd

FILE = 'ath_coe_centrality_features.txt'
FILE2 = 'ath_coe_clusters.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

'''
df
Out[3]: 
           coe_deg_cen   coe_bet_cen
Genes                               
AT1G06620     0.003292  1.100544e-04
AT1G28190     0.003334  9.442066e-05
AT5G55090     0.003463  1.117541e-04
AT5G12010     0.003292  9.189217e-05
AT5G19930     0.003078  6.308653e-05
               ...           ...
AT1G72760     0.000214  2.037764e-06
AT4G32690     0.000085  1.781436e-06
AT1G25220     0.000128  8.323878e-07
AT3G23630     0.000085  0.000000e+00
AT5G19200     0.000043  0.000000e+00

[23394 rows x 2 columns]

# Eyeball this in notepad+, various numbers seen in cluster_size
df2
Out[4]: 
           coe_cluster_size  ...  cid_cluster_id_99
Gene                         ...                   
AT5G37070               141  ...                  0
AT5G41240               141  ...                  0
AT4G14145               141  ...                  0
AT2G47700               141  ...                  0
AT1G13940               141  ...                  0
                    ...  ...                ...
AT4G12770               113  ...                  1
AT1G10290               113  ...                  1
AT1G80910               113  ...                  1
AT5G04420               113  ...                  1
AT3G16630               113  ...                  1

[24938 rows x 279 columns]
'''

