# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:24:56 2020

@author: weixiong001

Downcasts ml dataset datatypes to save memory
"""

import pandas as pd
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


print('Script started:', get_time())
ML_DATA = 'ml_16_labels.txt'
FILE = 'feature_type.txt'
OUTPUT = 'ml_16l_edited.txt'

data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
ft_df = pd.read_csv(FILE, sep='\t', index_col=0)

cont_feat = ft_df.loc[ft_df['Feature type'] == 'continuous', :].index
cat_feat = ft_df.loc[ft_df['Feature type'] == 'categorical', :].index
all_cont_feat = [x  for x in data.columns if (x.split('_')[0] + '_') in cont_feat]
all_cat_feat = [x for x in data.columns if (x.split('_')[0] + '_') in cat_feat]
class_labels = [x for x in data.columns if x.startswith('class_')]

data[all_cat_feat] = data[all_cat_feat].fillna(value=0)
temp = data[all_cat_feat].apply(pd.to_numeric, downcast='unsigned')
# takes ~1-2h, used modin!!
print('Operation started:', get_time())
data[all_cat_feat] = temp
print('Operation ended:', get_time())
temp2 = data[class_labels].apply(pd.to_numeric, downcast='unsigned')
data[class_labels] = temp2

data.to_csv(OUTPUT, na_rep='NA', sep='\t')
print('Script ended:', get_time())

'''
# Print out when script is ran to completion, takes ~1h
Script started: 26/11/2020 00:53:16
Operation started: 26/11/2020 00:54:14
Operation ended: 26/11/2020 01:45:08
Script ended: 26/11/2020 01:47:47
'''