# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:17:58 2022

@author: weixiong001

Exploring the results of the FRS calculations
"""

import pandas as pd

FILE = 'spearman_values.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
# 1800964
num_values = df.shape[0] * df.shape[1]
t = (df > 0).sum()
# 1771940
pos_values = t.sum()
# 98.38841864690244
percent_pos = pos_values/num_values * 100

neg_t = (df < 0).sum()
# 29024
neg_values = neg_t.sum()
# 1.6115813530975636
percent_neg = neg_values/num_values * 100


