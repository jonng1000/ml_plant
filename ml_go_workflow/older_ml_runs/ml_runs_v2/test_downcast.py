# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:34:46 2020

@author: weixiong001
"""

import pandas as pd

ML_DATA = 'ml_16l_edited.txt'
FILE = 'feature_type.txt'

data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
ft_df = pd.read_csv(FILE, sep='\t', index_col=0)

cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cat_feat]
class_labels = [x for x in data.columns if x.startswith('class_')]

uint8_mapping = all_cat_feat + class_labels
dtype_dict = {name:'uint8' for name in uint8_mapping}

df = pd.read_csv(ML_DATA, dtype=dtype_dict, sep='\t', index_col=0)

# Notes
# Downcasting works, but by default, pandas reads in values as float64
# and int64, so whenever I read in my ml data, need to specify
# dtypes as uint8 to preserve data
# Follow the above code to do this
# Verfied that the above code works, as I checked the columns of df
# and data to make sure it is as expected