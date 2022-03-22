# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis differential gene expression from Marek
and does one hot encoding according to a custom function. Environmental 
conditions where expression data are obtained from, are one hot encoded.
End product is saved to a new file. Edited from process_ath_exp.py
in /mnt/d/GoogleDrive/machine_learning/my_features/data_preprocessing
"""

import pandas as pd
import numpy as np

FILE = 'DGE'
OUTPUT = 'edited_Ath_dge.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.index = df.index.str.upper()

ohe_names = []
for name in df['Condition'].unique():
    name_up = name + '_up'
    name_down = name + '_down'
    ohe_names.append(name_up)
    ohe_names.append(name_down)

temp = list(df.columns)
temp.extend(ohe_names)
expanded_df = df.reindex(columns=temp)
significant_df = expanded_df.loc[expanded_df.loc[:, 'adj p-val'] < 0.05, :]
# All p-values are significant so dont need to do process this futther
# Still created this though, as a reminder to myself to process this
# if future data requires it
not_significant_df = expanded_df.loc[expanded_df['adj p-val'] >= 0.05, :]

# my function
def cust_ohe(my_row):
    condition = my_row.loc['Condition']
    if my_row.loc['log2 fold change'] > 0:
        my_row.loc[condition + '_up'] = 1
        my_row.loc[condition + '_down'] = 0
    elif my_row.loc['log2 fold change'] < 0:
        my_row.loc[condition + '_up'] = 0
        my_row.loc[condition + '_down'] = 1
    elif my_row.loc['log2 fold change'] == 0:
        my_row.loc[condition + '_up'] = 0
        my_row.loc[condition + '_down'] = 0
        print(my_row, 'has 0 log change')
    return my_row

mod_sdf = significant_df.apply(cust_ohe, axis=1)
com_df = pd.concat([mod_sdf, not_significant_df])
com_df.reset_index().groupby('Gene name').apply(lambda x : ' '.join(x))
com_df.drop(columns=['Condition', 'adj p-val', 'log2 fold change'], inplace=True)

def cust_combine(my_col):
    raise_error = True
    if my_col.isnull().all():
        value = np.nan
        raise_error = False
    else:
        for i in my_col:
            if i == 1.0:
                value = 1
                raise_error = False
                break
            elif i == 0.0:
                value = 0.0
                raise_error = False
                break
    if raise_error:        
        raise ValueError('1 or 0 not detected, and not values are np.nan')
    return value

final_df = com_df.reset_index().groupby('Gene name').\
           agg(lambda col: cust_combine(col))
final_df.rename(columns={x:'dge_' + x for x in final_df.columns}, inplace=True)
"""
# To test my custom combining function above
test = com_df.reset_index().groupby('Gene name').get_group('AT1G01030')
test_col = test['Ath_heat_up']
# Gives a rough idea of what is the correct df I expect, takes a single
# column, and combines all its values into a list
com_df.reset_index().groupby('Gene name').agg(lambda col: col.tolist())
"""

final_df.index.name = 'Gene'

final_df.to_csv(OUTPUT, sep='\t', na_rep='NA')
