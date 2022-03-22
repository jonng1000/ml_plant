# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/edited_Ath_jtk.txt'
OUTPUT = 'edited_Ath_jtk_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

# Temp list for Type column
temp_lst = ['Gene expression, diurnal timepoint (dit)'] * (len(df) - 1)
lst_values = ['Gene expression, diurnal amplitude (dia)'] + temp_lst
df.insert(loc=0, column='Type', value=lst_values)

# Temp list for Description column
temp_lst = ['Diurnal gene expresison'] * (len(df) - 1)
lst_values = ['Diurnal gene expresison'] + temp_lst
df.insert(loc=2, column='Description', value=lst_values)

df.to_csv(OUTPUT, sep='\t', index=False)

