# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Assembles all separate data files into one file for downstream ml work.
Modified from assemble_ml_data.py in 
D:\GoogleDrive\machine_learning\my_features\ml_runs_v2
Takes about 5 min
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

ft_df = pd.read_csv(FILE, sep='\t', index_col=0)

cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x  for x in df.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x + '_' for x in df.columns if (x.split('_')[0] + '_') in cat_feat]
'''
# ~30k genes, ~11k features
>>> df.shape
(30453, 11614)

# Shows the number of continuous and categorical features I have,
in total, I get the expected number from above
>>> len(all_cont_feat)
28
>>> len(all_cat_feat)
11149
'''

df.to_csv(OUTPUT, sep='\t')


