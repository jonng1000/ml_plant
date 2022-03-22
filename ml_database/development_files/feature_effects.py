# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:17:58 2022

@author: weixiong001

Calculating effect size and direction using Spearman's rank correlation 
coefficient
"""

import pandas as pd

FILE = 'selected_features.txt'
OUTPUT = 'spearman_values.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

ranks = df.rank(ascending=False, method='first')
"""
# This is just for testing
test = pd.DataFrame(data={'Animal': ['cat', 'penguin', 'dog',
                                     'spider', 'snake'],
                          'Number_legs': [4, 2, 4, 8, 0]})

test.rank(ascending=False, method='first')
"""
# Not calculating rho and p-values using stats.spearmanr() as its probably
# going to take 3-4h based on my draft script
# This takes 4 min to calculate
spearman_df = ranks.corr(method='spearman')

spearman_df.to_csv(OUTPUT, sep='\t')


