# -*- coding: utf-8 -*-
"""
Spyder Editor

Counts number of edges for each feature, this number is divided into same feature category,
different feature category, and same DGE experiment (0 for non-DGE features). Sorts features
according to number of edges, different category, descending order.
"""
import pandas as pd

FILE = 'overall_edges.csv'
FILE2 = 'sorted_dge_nodes_edges.txt'
FILE3 = 'new_names.txt'
OUTPUT = 'sorted_all_nodes_counts.txt'

df = pd.read_csv(FILE, sep=',', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
df3 = pd.read_csv(FILE3, sep='\t', index_col=0)

selected = df.loc[:, ['name']].copy()
selected['expt1_name'] = selected['name'].str.split(' \(-\) ').str[0]
selected['expt2_name'] = selected['name'].str.split(' \(-\) ').str[1]

expt1_prefix = selected['expt1_name'] .str.split('_').str[0]
expt2_prefix = selected['expt2_name'] .str.split('_').str[0]

selected['same_category'] = (expt1_prefix == expt2_prefix)
selected['diff_category'] = ~(expt1_prefix == expt2_prefix)

expt1 = selected.loc[:, ['expt1_name', 'same_category', 'diff_category']].copy()
expt2 = selected.loc[:, ['expt2_name', 'same_category', 'diff_category']].copy()
expt1.rename(columns={'expt1_name':'expt_name'}, inplace=True)
expt2.rename(columns={'expt2_name':'expt_name'}, inplace=True)

combined_df = pd.concat([expt1, expt2])
combined_df = combined_df.reset_index(drop=True)

edge_type_counts = combined_df.groupby(['expt_name']).sum()
edge_counts_dge = pd.concat([edge_type_counts, df2.loc[:, ['same_expt_DGE_category']]], axis=1)
edge_counts_dge['same_expt_DGE_category'] = edge_counts_dge['same_expt_DGE_category'].fillna(value=0)
sorted_edge_counts = edge_counts_dge.sort_values(by=['diff_category'], ascending=False)

sorted_edge_counts.to_csv(OUTPUT, sep='\t')