# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 17:51:37 2022

@author: weixiong001

Editing typos in nodes
"""

import pandas as pd

FILE = 'orig_nodes_network.csv'
FILE2 = 'typo_nodes_network.csv'
OUTPUT = 'corrected_typos_pre.txt'

df_orig = pd.read_csv(FILE, delimiter = ',')
df_typo = pd.read_csv(FILE2, delimiter = ',')

df_orig_name = df_orig.loc[:, ['name']]
df_orig_name['keys'] = df_orig['name'].str.replace('_', ' ')
df_orig_name.rename(columns={'name': 'name2'}, inplace=True)

df_typo['keys'] = df_typo['name'].str.replace('_', ' ')
corrected_df = df_typo.merge(df_orig_name, how='left', on='keys')

corrected_df.to_csv(OUTPUT, sep='\t')