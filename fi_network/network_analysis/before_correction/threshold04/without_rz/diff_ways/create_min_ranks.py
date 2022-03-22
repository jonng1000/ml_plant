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
OUTPUT = 'min_ranks.txt'

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
rank_pairs = pairs.groupby(pairs.index).min()

rank_df = rank_pairs.to_frame().reset_index()
rank_df[['f1', 'f2']] = pd.DataFrame(rank_df['index'].tolist(), index=rank_df.index)
rank_df.drop(columns=['index'], inplace=True)
rank_df = rank_df[rank_df.columns[[1,2,0]]]
rank_df.rename(columns={0: 'MinR'}, inplace=True)
print('Script ended:', get_time())
'''
# Max and min max rank respectively
rank_df['MinR'].max()
Out[53]: 926.5

rank_df['MinR'].min()
Out[54]: 1.0
'''
rank_df.index.name = 'id'
rank_df.to_csv(OUTPUT, sep='\t')
