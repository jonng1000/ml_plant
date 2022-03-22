# -*- coding: utf-8 -*-
"""
Spyder Editor

Counts number of DGE edges for each DGE feature, this number is divided into different 
DGE category, same DGE category, and same DGE experiment and category. Sorts features
according to number of edges, different category, descending order.
"""
import pandas as pd

FILE = 'edited_cytoscape_labels.txt'
FILE2 = 'DGE_names_status.txt'

df = pd.read_csv(FILE, sep='\t')
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
OUTPUT = 'dge_nodes_desc.txt'
OUTPUT2 = 'dge_nodes_edge_counts.txt'

selected = df.loc[:, ['name', 'full_expt1', 'full_expt2', 'edge_type']].copy()
selected['expt1_name'] = selected['name'].str.split(' \(-\) ').str[0]
selected['expt2_name'] = selected['name'].str.split(' \(-\) ').str[1]

expt1 = selected.loc[:, ['expt1_name', 'full_expt1', 'edge_type']].copy()
expt2 = selected.loc[:, ['expt2_name', 'full_expt2', 'edge_type']].copy()
expt1.rename(columns={'expt1_name':'expt_name', 'full_expt1':'expt_cat'}, inplace=True)
expt2.rename(columns={'expt2_name':'expt_name', 'full_expt2':'expt_cat'}, inplace=True)

combined_df = pd.concat([expt1, expt2])
combined_df = combined_df.reset_index(drop=True)
combined_df.insert(1, 'expt_desc', combined_df['expt_name'])
map_dict = pd.Series(df2['Specific_name'].values, index=df2['Experiment']).to_dict()
combined_df.replace({'expt_desc': map_dict}, inplace=True)
combined_df.index.name = 'id'

edge_type_counts = combined_df.groupby(['expt_name', 'edge_type']).size().unstack(fill_value=0)
edge_type_counts.insert(0, 'expt_desc', edge_type_counts.index)
edge_type_counts.replace({'expt_desc': map_dict}, inplace=True)
edge_type_counts.columns.name = None

combined_df.to_csv(OUTPUT, sep='\t')
edge_type_counts.to_csv(OUTPUT2, sep='\t')