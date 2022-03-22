# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Creates a list of the rest of categorical features
(non GO terms and DGE) as targets, to use for my ml workflow.
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
FT_FILE = '../feature_type.txt'
OUTPUT = 'class_labels_rcf.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
# Reads in the file with the types of features
ft_df = pd.read_csv(FT_FILE, sep='\t', index_col=0)

# Below 2 lines is just to check that dge_go_labels is done correctly
# 436 DGE labels
dge_labels = data.columns[data.columns.str.startswith('dge_')]
# 3645 GO labels
go_labels = data.columns[data.columns.str.startswith('go_')]

# Gets separate lists of continuous and categorical 
# 3155 cont labels
cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
# 8646 cat labels
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cat_feat]
selected = data.loc[:, all_cat_feat]
# 4565 non GO and DGE features for class labels
nt_dge_go = selected.columns[~selected.columns.str.startswith(('go_', 'dge_'))]

# To get class name as a column
# Reassigned variable to make my downsteam codee work
temp = nt_dge_go
temp_df = temp.to_frame(index=False)
df = temp_df.rename({0: 'catf_labels'}, axis='columns')

df.to_csv(OUTPUT, sep='\t', columns=['catf_labels'], header=False, index=False)
