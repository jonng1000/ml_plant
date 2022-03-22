# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Need to run on CN if input file takes up too much RAM
Explores mutual rank (MR) distribution  and obtain proportion 
of feature categories for high and low MR clusters
"""

import numpy as np
import pandas as pd

FILE = 'mutual_ranks.txt'
OUTPUT = 'prop_ab_740.txt'

# Cannot do the below due to some weird warnig
# FutureWarning: elementwise comparison failed; returning scalar instead,
# but in the future will perform
# elementwise comparison
# Something to do with a numpy and pandas clash, use the below workaround
#df = pd.read_csv(FILE, sep='\t', index_col=0)
df = pd.read_csv(FILE, sep='\t')
df.set_index(['id'], inplace=True)
sorted_df = df.sort_values(by=['MR'])

# From histogram, at around 740, it spikes up, resulting in an uneven
# distribution
above = sorted_df.loc[sorted_df['MR'] >= 740, :]
below = sorted_df.loc[~(sorted_df['MR'] >= 740), :]

pref_f1_above = above['f1'].str.split('_').str[0]
pref_f2_above = above['f2'].str.split('_').str[0]
above_vc = pd.concat([pref_f1_above, pref_f2_above]).value_counts()
above_vcn = pd.concat([pref_f1_above, pref_f2_above]).value_counts(normalize=True)

pref_f1_below = below['f1'].str.split('_').str[0]
pref_f2_below = below['f2'].str.split('_').str[0]
below_vc = pd.concat([pref_f1_below, pref_f2_below]).value_counts()
below_vcn = pd.concat([pref_f1_below, pref_f2_below]).value_counts(normalize=True)

prop_ab = pd.concat([above_vcn, below_vcn], axis=1)
prop_ab.rename(columns={0: 'above_thresh', 1: 'below_thresh'}, inplace=True)
prop_ab['prop_diff'] = prop_ab['above_thresh'] - prop_ab['below_thresh']
prop_ab.index.name = 'feature_cat'
prop_ab.to_csv(OUTPUT, sep='\t')
