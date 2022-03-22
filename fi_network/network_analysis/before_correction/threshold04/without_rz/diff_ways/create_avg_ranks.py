# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Takes about a few minutues
Creates avg ranks from selected features
"""

from datetime import datetime
from scipy import stats
import pandas as pd

FILE = 'impt_features_ranks.txt'
OUTPUT = 'avg_ranks.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

df = pd.read_csv(FILE, sep='\t', index_col=0)

'''
# Missing values as some features will not be assigned feature importance
# scores
df.isna().sum().sum()
Out[12]: 2988
'''
stacked = df.stack()

print('Script started:', get_time())
pairs = stacked[stacked.index.map(frozenset).duplicated(keep=False)]
pairs.index = pairs.index.map(frozenset)
# 1 049 756 rows after calculating mutual rank for each pair
# One row for each pair
mean_pairs = pairs.groupby(pairs.index).mean()

mean_df = mean_pairs.to_frame().reset_index()
mean_df[['f1', 'f2']] = pd.DataFrame(mean_df['index'].tolist(), index=mean_df.index)
mean_df.drop(columns=['index'], inplace=True)
mean_df = mean_df[mean_df.columns[[1,2,0]]]
mean_df.rename(columns={0: 'AR'}, inplace=True)
print('Script ended:', get_time())
'''
# Max and min avg rank respectively
>>> mean_df['AR'].max()
1088.0
>>> mean_df['AR'].min()
1.0
'''
mean_df.index.name = 'id'
mean_df.to_csv(OUTPUT, sep='\t')
