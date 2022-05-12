# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:00:24 2022

@author: weixiong001

Explores HP optimisation results
"""

import pandas as pd

FILE = 'all_data_plotting.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

'''
# Shows avg F1 score (value)

df.groupby('hp_type').mean()
Out[5]: 
                 value
hp_type               
chosen        0.415040
chosen_g1     0.415050
chosen_g2     0.415357
default       0.086755
rs_optimised  0.459666
'''