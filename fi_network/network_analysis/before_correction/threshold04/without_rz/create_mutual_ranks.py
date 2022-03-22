# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Takes about a few minutues
Creates mutual ranks from selected features
"""

from datetime import datetime
from scipy import stats
import pandas as pd

FILE = 'impt_features_ranks.txt'
OUTPUT = 'mutual_ranks.txt'

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
gmean_pairs = pairs.groupby(pairs.index).apply(stats.gmean)

gmean_df = gmean_pairs.to_frame().reset_index()
gmean_df[['f1', 'f2']] = pd.DataFrame(gmean_df['index'].tolist(), index=gmean_df.index)
gmean_df.drop(columns=['index'], inplace=True)
gmean_df = gmean_df[gmean_df.columns[[1,2,0]]]
gmean_df.rename(columns={0: 'MR'}, inplace=True)
print('Script ended:', get_time())
'''
# Number of rows for each feature pair
>>> gmean_df.shape
(1049756, 3)
# Max and min mutual rank respectively
>>> gmean_df['MR'].max()
1045.8549134559719
>>> gmean_df['MR'].min()
1.0
'''
gmean_df.index.name = 'id'
gmean_df.to_csv(OUTPUT, sep='\t')
