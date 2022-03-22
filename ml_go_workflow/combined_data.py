# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:08:54 2021

@author: weixiong001

Combines all feature files to form complete dataset

Takes 8min to run, 7min is spent writing the file
"""

import os
import pandas as pd

# Base path for all data files
PATH = './all_data/'
FILE = 'feature_type.txt'
OUTPUT = 'ml_dataset.txt'

df_lst = []
for f in os.listdir(PATH):
    a_df = pd.read_csv(PATH+f, sep='\t', index_col=0)
    df_lst.append(a_df)
    
df = pd.concat(df_lst, axis=1)
df.index.name = 'Gene'

'''
# Earlier had duplicate genes issue, problem was in tf-tg coexp features
# file, but corrected it
for x in range(len(df_lst)):
    print(x)
    print(len(df_lst[x].index))
    print(len(set(df_lst[x].index)))
    print()
'''

# Tests to see proportion of nan for ATXG and non ATXG gene names
# Not impt
test1 = df.loc[df.index.str.startswith('AT'), :]
'''
test1.isna().sum().sum()
Out[40]: 150058957
test1.size
Out[41]: 364025447
150058957/364025447
Out[43]: 0.41222106376535816
'''
test2 = df.loc[~df.index.str.startswith('AT'), :]
'''
test2.isna().sum().sum()
Out[51]: 6145084
test2.size
Out[52]: 7965675
6145084/7965675
Out[53]: 0.771445483276684
'''

'''
# Tests to see how many non ATXG gene names are there, but this is not impr
for x in range(len(df_lst)):
    print(x)
    print(df_lst[x].head())
    temp = set([y[:4] for y in df_lst[x].index])
    if len(temp) == 7:
        print(temp)
    print()

9,21,22,24,25 : < 7, but its ok, all ATXG names
3,8,10; non ATXG name starts with Arth
12,20: quite a lot of non ATXG names
3,8,9,10,12,20,21,22,24,25
'''

ft_df = pd.read_csv(FILE, sep='\t', index_col=0)
cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x  for x in df.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x + '_' for x in df.columns if (x.split('_')[0] + '_') in cat_feat]
'''
# Shows how many categorical and continous features I have
len(all_cat_feat)
Out[112]: 8700

len(all_cont_feat)
Out[113]: 3101
'''
'''
# Exploring data, seeing proportion of nan
df.shape
Out[115]: (31525, 11801)

df.isnull().sum().sum()
Out[116]: 156239444

156239444 / (df.shape[0] * df.shape[1]) * 100
Out[117]: 41.996856003748654
'''
'''
# Put this here to make sure the number of prefixes is as expected
# Previously tti prefix didnt exist as these features would have been
# wrongly assigned to ttr
# Edited 170821
set(df.columns.str.split('_').str[0])
Out[215]: 
{'agi',
 'agn',
 'cid',
 'cif',
 'cin',
 'coe',
 'con',
 'dge',
 'dia',
 'dit',
 'gbm',
 'go',
 'gwa',
 'hom',
 'mob',
 'ntd',
 'num',
 'ort',
 'pep',
 'pfa',
 'phy',
 'pid',
 'ppi',
 'ptm',
 'sin',
 'spm',
 'tan',
 'tmh',
 'tpm',
 'ttf',
 'tti',
 'ttr',
 'twa'}

len(set(df.columns.str.split('_').str[0]))
Out[216]: 33
'''

df.to_csv(OUTPUT, sep='\t')
