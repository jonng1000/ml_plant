# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 17:00:12 2021

@author: weixiong001

Check continuous features for wrongly labelled ttr_cluster_id features and
removes them
"""

import pandas as pd

FILE = 'score04_contf_features.txt'
OUTPUT = 'score04edit_contf_features.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# 14 out of 175 continuous features are the incorrectly labelled
# ttr_cluster_id features, they should have been tti_cluster_id features
df.index[df.index.str.startswith('ttr_cluster_id')]
Out[48]: 
Index(['ttr_cluster_id_1', 'ttr_cluster_id_2', 'ttr_cluster_id_3',
       'ttr_cluster_id_4', 'ttr_cluster_id_5', 'ttr_cluster_id_6',
       'ttr_cluster_id_7', 'ttr_cluster_id_8', 'ttr_cluster_id_9',
       'ttr_cluster_id_12', 'ttr_cluster_id_13', 'ttr_cluster_id_14',
       'ttr_cluster_id_18', 'ttr_cluster_id_21'],
      dtype='object', name='class_label')

len(df.index[df.index.str.startswith('ttr_cluster_id')])
Out[49]: 14
'''

new_df = df.loc[~df.index.str.startswith('ttr_cluster_id'), :]
new_df.to_csv(OUTPUT, sep='\t')
