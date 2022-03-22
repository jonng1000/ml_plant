# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:17:58 2022

@author: weixiong001

Data preprocessing to determine effect sizes between features and targets in 
the feature network. Select only those features in the network, then fill
missing continuous features with mean, and categorical features with 0.
"""

import pandas as pd
from scipy import stats

FILE = 'G:/My Drive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
FILE2 = 'G:/My Drive/machine_learning/fi_network/network_analysis/selected_mr.txt'
FILE3 = 'G:/My Drive/machine_learning/ml_go_workflow/feature_type.txt'
OUTPUT = 'selected_features.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
ft_df = pd.read_csv(FILE3, sep='\t', index_col=0)

append_series = pd.concat([df2['f1'], df2['f2']])
features = append_series.drop_duplicates()
features_df = df.loc[:, features]

# Gets separate lists of continuous and categorical features
cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x for x in features_df.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x  for x in features_df.columns if (x.split('_')[0] + '_') in cat_feat]

cont_fdf = features_df.loc[:, all_cont_feat]
cat_fdf = features_df.loc[:, all_cat_feat]

filled_cont_df = cont_fdf.fillna(cont_fdf.mean())
filled_cat_df = cat_fdf.fillna(0)
selected_feat = pd.concat([filled_cont_df, filled_cat_df], axis=1)

selected_feat.to_csv(OUTPUT, sep='\t')