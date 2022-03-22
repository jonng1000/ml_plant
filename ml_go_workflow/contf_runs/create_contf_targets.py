# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Creates a list of continuous feastures as class targets, to use for my
ml workflow.
"""

import pandas as pd
# ml_dataset_mod.txt
FILE = '../ml_dataset_dc.txt'  # Original dataset '../ml_dataset_dc.txt'
FT_FILE = '../feature_type.txt'
OUTPUT = 'class_labels_contf.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
# Reads in the file with the types of features
ft_df = pd.read_csv(FT_FILE, sep='\t', index_col=0)

# Gets separate lists of continuous and categorical 
# 3155 cont labels
cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
# 8646 cat labels
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cat_feat]
selected = data.loc[:, all_cont_feat]

# To get class name as a column
# Reassigned variable to make my downsteam codee work
temp = selected.columns
temp_df = temp.to_frame(index=False)
df = temp_df.rename({0: 'contf_labels'}, axis='columns')

df.to_csv(OUTPUT, sep='\t', columns=['contf_labels'], header=False, index=False)
