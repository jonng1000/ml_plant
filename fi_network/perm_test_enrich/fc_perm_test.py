# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 17:16:05 2021

@author: weixiong001

Permutation test to see if proportion of feature categories in clusters is statistically
significant
"""

import pandas as pd
import numpy as np
from datetime import datetime

FILE = 'feat_cat_info.txt'
FILE2 = 'categories_orig_prop.txt'
OUTPUT = 'pvalue_fcat_test.txt'
NUM = 10000  # Takes 30s

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

counts_larger = pd.DataFrame(0, columns=df2.columns, index=df2.index)

print('Script started:', get_time())
for i in range(NUM):
    df['feat_category'] = np.random.permutation(df['feat_category'])
    # Copied from cal_ofc_prop.py
    cat_counts = df.groupby(['feat_cluster_id', 'feat_category']).size()\
        .unstack(fill_value=0)
    cat_counts.columns.name = None
    cat_prop = cat_counts.copy()
    total_value = cat_prop.sum(axis=1)
    cat_prop = cat_prop.divide(total_value, axis=0)
    # Checks to see if original proportion is higher than permutated
    # proportion
    temp = df2 > cat_prop
    temp = temp.astype(int)
    counts_larger = counts_larger + temp
print('Script ended:', get_time())

# 0 -> original proportion is always lower than permutated proportion
# 1 -> original proportion is always higher than permutated proportion
p_value = counts_larger/10000

p_value.to_csv(OUTPUT, sep='\t')