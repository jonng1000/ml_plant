# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:17:58 2022

@author: weixiong001

Doing spearman correlation for continuous vs continuous features. Partially
done and stopped because this is not the method which we are using to
determine effect sizes between features and targets in the feature network.
"""

import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

FILE = 'G:/My Drive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
FILE2 = 'G:/My Drive/machine_learning/fi_network/network_analysis/selected_mr.txt'
FILE3 = 'G:/My Drive/machine_learning/ml_go_workflow/feature_type.txt'

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
# Takes about 15 min
rho, pval = stats.spearmanr(cont_fdf, nan_policy='omit')

rho_df = pd.DataFrame(index=cont_fdf.columns, columns=cont_fdf.columns, data=rho)
pval_df = pd.DataFrame(index=cont_fdf.columns, columns=cont_fdf.columns, data=pval)
pval_stack = pval_df.stack()
# BH correction of p value
bh_correction = multipletests(pvals=pval_stack, alpha=0.05, method='fdr_bh')
