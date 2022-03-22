# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:35:20 2021

@author: weixiong001

Calculates number of edges between feature category pairs
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/fi_network/network_analysis/selected_mr.txt'
FILE2 = 'feature_category_info.txt'
OUTPUT = 'edges_catgories.txt'


df = pd.read_csv(FILE, sep='\t', index_col=0)
df = df.rename(columns={'f1': 'source', 'f2': 'target'})

df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
feat_cat_dict = df2['feat_category'].to_dict()

df_feat_cat = df.replace(feat_cat_dict)
df_feat_cat['pairs'] = df_feat_cat[['source', 'target']].apply(frozenset, axis=1)
edges_across = df_feat_cat.groupby('pairs').size().reset_index()
edges_across.rename(columns={0:'number_edges'}, inplace=True)
sorted_edges = edges_across.sort_values(by=['number_edges'], ascending=False)
sorted_edges = sorted_edges.reset_index()
sorted_edges[['category_1', 'category_2']] = pd.DataFrame(sorted_edges['pairs'].tolist(), index=sorted_edges.index)
dropped_edges = sorted_edges.drop(columns=['index', 'pairs'])
dropped_edges = dropped_edges.loc[:, ['category_1', 'category_2', 'number_edges']]
filled_none = dropped_edges.ffill(axis=1)

filled_none.index.name = 'id'
filled_none.to_csv(OUTPUT, sep='\t')