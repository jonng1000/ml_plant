# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/cis_features.txt'
OUTPUT = 'cis_features_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

df.insert(loc=0, column='Type', value='PLACEHOLDER')
df.insert(loc=2, column='Description', value='PLACEHOLDER')
df.loc[df['ID'].str.startswith('cin'), 'Type'] = 'cis-regulatory element names (cin)'
df.loc[df['ID'].str.startswith('cif'), 'Type'] = 'cis-regulatory element families (cif)'
df.loc[df['ID'].str.startswith('cin'), 'Description'] = 'Gene regulation'
df.loc[df['ID'].str.startswith('cif'), 'Description'] = 'Gene regulation'

'''
# Just to check to ensure adding of values to columns is done correctly
>>> set(df['Type'])
{'cis-regulatory element families (cif)', 'cis-regulatory element names (cin)'}
>>> set(df['Description'])
{'Gene regulation'}
'''

df.to_csv(OUTPUT, sep='\t', index=False)

