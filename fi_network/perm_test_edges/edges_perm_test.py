# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 17:16:05 2021

@author: weixiong001

Permutation test to see if number of edges across feature categories
is statistically significant
"""

import pandas as pd
import numpy as np
from datetime import datetime

FILE = 'D:/GoogleDrive/machine_learning/fi_network/network_analysis/selected_mr.txt'
FILE_SUPP = 'feature_category_info.txt'
FILE2 = 'edges_catgories.txt'
OUTPUT = 'pvalue_edges.txt'
NUM = 10000  # Takes abt 10 min

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Read in dfs
# Feature pairs with mutual ranks (MR)
df = pd.read_csv(FILE, sep='\t', index_col=0)
df = df.rename(columns={'f1': 'source', 'f2': 'target'})
# Feature category names
df_supp = pd.read_csv(FILE_SUPP, sep='\t', index_col=0)
# Original number of edges per feature category pair
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

# Original data of edges between feature categories
feat_cat_dict = df_supp['feat_category'].to_dict()
df_feat_cat = df.replace(feat_cat_dict)
orig_feat = df_feat_cat.copy()

# Original number of edges per feature category pair,
# formatted into frozen sets
df2['pairs'] = df2[['category_1', 'category_2']].apply(frozenset, axis=1)
dropped_df2 = df2.drop(columns=['category_1', 'category_2'])
dropped_df2 = dropped_df2.set_index('pairs')

# Permutation test
print('Script started:', get_time())
lst_counts = []
for i in range(NUM):
    # Need to randomly shuffle each column individually
    orig_feat['source'] = np.random.permutation(df_feat_cat['source'])
    orig_feat['target'] = np.random.permutation(df_feat_cat['target'])
    orig_feat['pairs'] = orig_feat[['source', 'target']].apply(frozenset, axis=1)
    # Counts edges after permutation
    edges_perm = orig_feat.groupby('pairs').size().reset_index()
    edges_perm.rename(columns={0:'number_edges'}, inplace=True)
    edges_perm = edges_perm.set_index('pairs')
    # Assembling a temp df to compare
    combined = pd.concat([dropped_df2, edges_perm], axis=1)
    combined.fillna(0, inplace=True)    
    combined.columns = ['number_orig', 'number_perm']
    combined['diff'] = combined['number_orig'] - combined['number_perm']
    # Determines if original number of edges is higher than the permutated one
    one_count = (combined['diff'] > 0).astype(int)
    lst_counts.append(one_count)

# Assembling counts from all permutations
all_counts = pd.concat(lst_counts, axis=1)
total_value = all_counts.sum(axis=1)
# Calculating p values
p_value = total_value/NUM
# Formatting p values to save to file
p_value = p_value.reset_index()
p_value[['category_1', 'category_2']] = pd.DataFrame(p_value['pairs'].tolist())
p_value.drop(columns=['pairs'], inplace=True)
p_value.rename(columns={0: 'p_value'}, inplace=True)
p_value = p_value.loc[:, ['category_1', 'category_2', 'p_value']]
p_value = p_value.ffill(axis=1)
p_value.index.name = 'id'

print('Script ended:', get_time())
# 0 -> original proportion is always lower than permutated proportion
# 1 -> original proportion is always higher than permutated proportion
p_value.to_csv(OUTPUT, sep='\t')
