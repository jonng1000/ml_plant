# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/tt_coexp_features.txt'
OUTPUT = 'tt_coexp_features_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

# Temp list for Type column
temp_lst = ['Properties of transcription factors and their target genes - transcription factor-target gene features (ttf)'] * len(df)
df.insert(loc=0, column='Type', value=temp_lst)

# Temp list for Description column
temp_lst = ['Biological characteristics of transcription factors and their target genes as recorded in the paper'] * len(df)
df.insert(loc=2, column='Description', value=temp_lst)

df.to_csv(OUTPUT, sep='\t', index=False)

