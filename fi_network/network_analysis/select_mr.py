# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:49:11 2021

@author: weixiong001

Selects features based on mutual rank (MR) threshold
"""


import pandas as pd

FILE = 'nonzero_mr.txt'
OUTPUT = 'selected_mr.txt'


df = pd.read_csv(FILE, sep='\t', index_col=0)
sorted_df = df.sort_values(by=['MR'])
'''
# Total number of edges
len(sorted_df)/10
Out[22]: 5308.1
# Top 10% would be 5308
'''

top = sorted_df[:5308]
top = top.reset_index()
top.drop(columns=['id'], inplace=True)
top.index.name = 'id'
top['invert_ranks'] = top['MR'].values[::-1]

top.to_csv(OUTPUT, sep='\t')