# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 19:44:04 2021

@author: weixiong001

Annotates DGE expts, whether they are from the same category and/or expt or not 
"""

import pandas as pd
import numpy as np

FILE = 'DGE_edges_cytoscape.csv'
FILE2 = 'dge_network_node.csv'
OUTPUT = 'edited_cytoscape_labels.txt'

df = pd.read_csv(FILE, sep=',')
df2 = pd.read_csv(FILE2, sep=',')

expt1 = df['shared name'].str.split(" \(-\) ").str[0]
expt1 = expt1.str.split('_').str[1]
expt2 = df['shared name'].str.split(" \(-\) ").str[1]
expt2 = expt2.str.split('_').str[1]

df['full_expt1'] = df['shared name'].str.split(" \(-\) ").str[0]
df['full_expt2'] = df['shared name'].str.split(" \(-\) ").str[1]

map_dict = pd.Series(df2['feat_category'].values, index=df2['name']).to_dict()
replaced_df = df.replace({'full_expt1': map_dict, 'full_expt2': map_dict})
replaced_df['edge_type'] = np.nan
replaced_df.loc[replaced_df['full_expt1'] == replaced_df['full_expt2'], 'edge_type'] = 'same_DGE_category'
replaced_df.loc[~(replaced_df['full_expt1'] == replaced_df['full_expt2']), 'edge_type'] = 'diff_DGE_category'
replaced_df.loc[(expt1 == expt2), 'edge_type'] = 'same_expt_DGE_category'

replaced_df.to_csv(OUTPUT, sep='\t', index=False)
'''
replaced_df.isna().any().any()
Out[328]: False
'''
