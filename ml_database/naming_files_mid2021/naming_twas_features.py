# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/twas_features.txt'
OUTPUT = 'twas_features_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

# Temp list for Type column
temp_lst = ['phenotype traits  - transcriptome wide association (twa)'] * len(df)
df.insert(loc=0, column='Type', value=temp_lst)

# Temp list for Description column
temp_lst = ['Gene expression level, correlated with phenotype traits'] * len(df)
df.insert(loc=2, column='Description', value=temp_lst)

df.to_csv(OUTPUT, sep='\t', index=False)

