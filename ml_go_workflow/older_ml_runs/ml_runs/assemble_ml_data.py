# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Assembles all separate data files into one file for downstream ml work.
Takes about 3 min
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
# Note 251120, not sure why there's '_' below, could be an error, anyway this script
# works so its fine. Future uses of this code have corrected this
all_cat_feat = [x + '_' for x in df.columns if (x.split('_')[0] + '_') in cat_feat]
'''
# ~29k genes, ~6k features
>>> df.shape
(29924, 6433)
# ~190 m values
>>> df.shape[0] * df.shape[1]
192 501 092
# ~66 m NA values, however, NA values in DGE, and gene coexpression
# cluster ids, have been filled in with 0
>>> df.isnull().sum().sum()
66 332 994
# ~34% of values are missing, but with the above caveat
>>> df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
34.45850270813009

# To see the set of different feature categories I have
>>> set([x.split('_')[0] for x in df.columns])
{'pep', 'ppi', 'tmh', 'ort', 'dit', 'dge', 'phy', 'pid', 'tpm', 'cid', 'sin', 'spm', 'tan', 'mob', 'pfa', 'dia', 'coe', 'num'}

# Shows the number of continuous and categorical features I have,
in total, I get the expected number from above
>>> len(all_cont_feat)
28
>>> len(all_cat_feat)
6405
'''

df.to_csv(OUTPUT, sep='\t', na_rep='NA')


