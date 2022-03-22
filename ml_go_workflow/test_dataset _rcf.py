# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 23:12:53 2021

@author: weixiong001

Creates a test dataset for testing my ml workflow, for non GO and DGE class
labels
"""

import pandas as pd

FILE = 'ml_dataset_dc.txt'
FT_FILE = 'feature_type.txt'
OUTPUT = 'test_dataset_rcf.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
# Reads in the file with the types of features
ft_df = pd.read_csv(FT_FILE, sep='\t', index_col=0)

# Gets separate lists of continuous and categorical features
cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cat_feat]

selected = data.loc[:, all_cat_feat]
# 4565 non GO and DGE features for class labels
nt_dge_go = selected.loc[:, ~selected.columns.str.startswith(('go_', 'dge_'))]
'''
# Eg of class labels
agi_cluster_id_1, agi_cluster_id_100
'''

small = nt_dge_go.iloc[:100, :100]
small.to_csv(OUTPUT, sep='\t')
