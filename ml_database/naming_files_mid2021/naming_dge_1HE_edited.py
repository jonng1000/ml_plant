# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/dge_1HE_edited.txt'
OUTPUT = 'dge_1HE_edited_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

df.insert(loc=0, column='Type', value='Gene expression')
df.insert(loc=2, column='Description', value='Differential levels of gene expression')

df.to_csv(OUTPUT, sep='\t', index=False)

