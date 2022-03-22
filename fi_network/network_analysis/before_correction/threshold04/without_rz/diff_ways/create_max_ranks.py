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
OUTPUT = 'max_ranks.txt'

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
rank_pairs = pairs.groupby(pairs.index).max()

rank_df = rank_pairs.to_frame().reset_index()
rank_df[['f1', 'f2']] = pd.DataFrame(rank_df['index'].tolist(), index=rank_df.index)
rank_df.drop(columns=['index'], inplace=True)
rank_df = rank_df[rank_df.columns[[1,2,0]]]
rank_df.rename(columns={0: 'MaxR'}, inplace=True)
print('Script ended:', get_time())
'''
# Max and min max rank respectively
>>> rank_df['MaxR'].max()
1088.0
>>> rank_df['MaxR'].min()
1.0

rank_df.loc[rank_df['MaxR'] == 1, :]
Out[41]: 
                               f1                        f2  MaxR
4369                go_GO:0034756             go_GO:0051050   1.0
8262                go_GO:0031669             go_GO:0042594   1.0
20439               go_GO:0046983             go_GO:0042802   1.0
24595               go_GO:0043254             go_GO:0051493   1.0
25176               go_GO:0048509             go_GO:0040034   1.0
                          ...                       ...   ...
1040747   dge_E-GEOD-77017_4_down   dge_E-GEOD-77017_2_down   1.0
1042262    dge_E-GEOD-75933_2a_up    dge_E-GEOD-75933_2b_up   1.0
1043959  dge_E-GEOD-75933_2b_down  dge_E-GEOD-75933_2a_down   1.0
1045752    dge_E-GEOD-75933_3b_up    dge_E-GEOD-75933_3a_up   1.0
1048923  dge_E-GEOD-75933_3b_down  dge_E-GEOD-75933_3a_down   1.0

[132 rows x 3 columns]
'''
rank_df.index.name = 'id'
rank_df.to_csv(OUTPUT, sep='\t')
