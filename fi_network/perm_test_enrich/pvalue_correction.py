# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 11:25:26 2021

@author: weixiong001

Applies pvalue correction after permutation test
"""

import pandas as pd

FILE = 'pvalue_fcat.txt'
OUTPUT = 'pvalue_corrected.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# Number to multiply for bonferroni correction
df.size
Out[233]: 4140
'''
enriched_df = 1 - df

depleted_corr = df * 4140
enriched_corr = enriched_df * 4140
de_bool = depleted_corr < 0.05
en_bool = enriched_corr < 0.05
'''
# Checks to ensure True values are unique in these two masks
(en_bool & de_bool).any().any()
Out[262]: False
'''
# 1 means enriched, -1 means depleted
en_pos1 = en_bool.astype(int)
de_neg1 = de_bool.astype(int)
de_neg1 = de_neg1 * -1
comb_sign = (en_pos1 + de_neg1).transpose()
comb_sign.columns.name = None
comb_sign.index.name = 'feature_category'

comb_sign.to_csv(OUTPUT, sep='\t')
