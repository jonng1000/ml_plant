# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/edited_Ath_protein_doms.txt'
OUTPUT = 'edited_Ath_protein_doms.txt_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

# Temp list for Type column
temp_lst = ['Protein domain'] * (len(df) - 4)
# This has 4 of the same values, just to help me see that these four features are different from the
# above features which all belong to the same type
lst_values = temp_lst + ['Protein domain', 'Protein domain', 'Protein domain', 'Protein domain']
df.insert(loc=0, column='Type', value=lst_values)

# Temp list for Description column
temp_lst = ['Collection of protein families, represented by hidden Markov models (HMMs)'] * (len(df) - 4)
lst_values = temp_lst + ['Number of protein domains, including repeated domains',
                         'Number of protein domains, excluding repeated domains',
                         'Prediction of disordered domains regions', 'Prediction of transmembrane helices']
df.insert(loc=2, column='Description', value=lst_values)

df.to_csv(OUTPUT, sep='\t', index=False)

