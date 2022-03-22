# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:20:51 2019

@author: weixiong001
"""

import pandas as pd
import numpy as np
import csv
import itertools

df = pd.read_csv('genes_lca.txt', sep='\t', index_col=0)
taxa_genes = df.groupby('Category')['taxon'].value_counts()
prop_GMSMnl = taxa_genes.groupby(level=0).apply(lambda x: x/x.sum())
all_zeroes = prop_GMSMnl.copy()
all_zeroes[all_zeroes < 1] = 0

# Here shows original ratios
#prop_GMSMnl
#Out[67]: 
#Category  taxon        
#GM        viridiplantae    0.730094
#          embryophyte      0.236842
#          angiosperm       0.020918
#          eudicot          0.012146
#SM        viridiplantae    0.570175
#          embryophyte      0.350877
#          eudicot          0.052632
#          angiosperm       0.026316
#no_label  viridiplantae    0.468318
#          embryophyte      0.330424
#          eudicot          0.136653
#          angiosperm       0.064604
#Name: taxon, dtype: float64

list_ratios = []
num = 2
for i in range(num):
    df['taxon'] = np.random.permutation(df['taxon'])
    shuffled = df.groupby('Category')['taxon'].value_counts()
    prop_shuffled = shuffled.groupby(level=0).apply(lambda x: x/x.sum())
    
    for i in prop_shuffled.index:
        if prop_shuffled.loc[i] > prop_GMSMnl.loc[i]:
            all_zeroes.loc[i] += 1
    list_ratios.append(prop_shuffled)
    p_value = all_zeroes/num
    
ratios_df = pd.concat(list_ratios, axis=1)
abc
# p-values after shuffling
#p_value
#Out[64]: 
#Category  taxon        
#GM        viridiplantae    0.0000
#          embryophyte      1.0000
#          angiosperm       1.0000
#          eudicot          1.0000
#SM        viridiplantae    0.0285
#          embryophyte      0.2439
#          eudicot          0.9930
#          angiosperm       0.9279
#no_label  viridiplantae    1.0000
#          embryophyte      0.0000
#          eudicot          0.0000
#          angiosperm       0.0000
#Name: taxon, dtype: float64

avg_ratios = ratios_df.sum(axis=1)/num
# Here shows average ratios after 10 000 permutations
#ratios_df.sum(axis=1)/num
#Out[117]: 
#Category  taxon        
#GM        angiosperm       0.061934
#          embryophyte      0.325121
#          eudicot          0.129172
#          viridiplantae    0.483773
#SM        angiosperm       0.062379
#          embryophyte      0.325160
#          eudicot          0.129191
#          viridiplantae    0.483270
#no_label  angiosperm       0.061920
#          embryophyte      0.325135
#          eudicot          0.129119
#          viridiplantae    0.483826
#dtype: float64

transposed_df = ratios_df.T

for col in transposed_df.columns:
    print(col)
    transposed_df[(col[0], col[1] + '_divided')] = \
    prop_GMSMnl[col]/transposed_df[col]
    transposed_df[(col[0], col[1] + '_change_log2')] = \
    transposed_df[(col[0], col[1] + '_divided')].apply(np.log2)
    
transposed_df.to_csv('procesed_ratios_lca.txt', sep='\t')

