# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Test script for building network (actually it means calculating mutual ranks)
"""

from scipy import stats
import pandas as pd

FILE = 'feature_ranks.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

'''
# Missing values as some features will not be assigned feature importance
# scores
df.isna().sum().sum()
Out[12]: 24674
'''

stacked = df.stack()

temp = stacked.loc[[('go_GO:0000030', 'go_GO:0022414'), 
                    ('go_GO:0022414', 'go_GO:0000030'), 
                    ('go_GO:0022414', 'go_GO:0000096'),
                    ('go_GO:0022414', 'go_GO:0000041'), 
                    ('go_GO:0000041', 'go_GO:0022414')], ]
pairs = temp[temp.index.map(frozenset).duplicated(keep=False)]
pairs.index = pairs.index.map(frozenset)
gmean_pairs = pairs.groupby(pairs.index).apply(stats.gmean)
gmean_df = gmean_pairs.to_frame().reset_index()
gmean_df[['f1', 'f2']] = pd.DataFrame(gmean_df['index'].tolist(), index=gmean_df.index)
gmean_df.drop(columns=['index'], inplace=True)
gmean_df = gmean_df[gmean_df.columns[[1,2,0]]]
gmean_df.rename(columns={0: 'MR'}, inplace=True)
