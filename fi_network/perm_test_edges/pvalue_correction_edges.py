# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 11:25:26 2021

@author: weixiong001

Applies pvalue correction after permutation test.
Uses Benjamini-Hochberg correction
"""

import pandas as pd
from statsmodels.stats.multitest import multipletests

FILE = 'pvalue_edges.txt'
OUTPUT = 'pvalue_corrected.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

depleted_bh = multipletests(pvals=df['p_value'], alpha=0.05, method='fdr_bh')
depleted_corr = depleted_bh[1]
df['enriched_p'] = 1 - df['p_value']
enriched_bh = multipletests(pvals=df['enriched_p'], alpha=0.05, method='fdr_bh')
enriched_corr = enriched_bh[1]
# 1 means enriched, -1 means depleted
de_neg1 = depleted_bh[0].astype(int)
de_neg1 = de_neg1 * -1
en_pos1 = enriched_bh[0].astype(int)
comb_sign = en_pos1 + de_neg1
'''
# Checks to ensure True values are unique in these two masks
(en_bool & de_bool).any().any()
Out[262]: False
'''
df['corrected_result'] = comb_sign
dropped = df.drop(columns=['p_value', 'enriched_p'])
dropped.to_csv(OUTPUT, sep='\t')
