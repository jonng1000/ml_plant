# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 23:12:53 2021

@author: weixiong001

Basic exploration of ml dataset
"""

import pandas as pd

FILE = 'ml_dataset_dc.txt'
FILE2 = 'feature_type.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
ft_df = pd.read_csv(FILE2, sep='\t', index_col=0)

cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cat_feat]
'''
# Dimensons of the dataframe
data.shape
Out[54]: (31525, 11801)
# Number of continuous and categorical features
len(all_cont_feat)
Out[59]: 3101
len(all_cat_feat)
Out[60]: 8700
'''
