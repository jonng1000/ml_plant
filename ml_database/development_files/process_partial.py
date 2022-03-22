# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 17:54:07 2021

@author: weixiong001

Renaming type, name and description of features for both global feature table,
and local feature table (local feature network) for database
IMPT: partially done as I realised its easier to do this manually in Excel

Takes in an earlier version of such a file, combined_names_v2.txt, from
G:/My Drive/machine_learning/ml_database
"""

import pandas as pd

FILE = 'G:/My Drive/machine_learning/ml_database/combined_names_v2.txt'
OUTPUT = 'partial.txt'


df = pd.read_csv(FILE, sep='\t', index_col=0)
df.sort_values(by=['ID'], inplace=True)

# Aranet features
new_df = df.rename(index={'Functional gene network - number of gene interactions of a given gene (Aranet gene network - agn)': 
                          'Aranet, functional gene network features (agn)'})
new_df.loc[new_df['ID'] == 'agn_deg_cen', 'Description'] = 'Node degree'
new_df.loc[new_df['ID'] == 'agn_bet_cen', 'Description'] = 'Node betweeness centrality'
new_df.rename(index={'Functional gene network - cluster id (agi)': 
                     'Aranet, functional gene network clusters (agi)'}, inplace=True)
new_df.loc[new_df['ID'].str.startswith('agi_cluster_id'), 'Description'] = 'Cluster id'
new_df.rename(index={'Functional gene network - cluster size (agn)': 
                     'Aranet, functional gene network features (agn)'}, inplace=True)
new_df.loc[new_df['ID'].str.startswith('agn_cluster_size'), 'Description'] = 'Cluster size'
# Biochemical features
new_df.rename(index={'Functional gene network - cluster size (agn)': 
                     'Aranet, functional gene network features (agn)'}, inplace=True)
# Gene coexp features
new_df.rename(index={'Network clusters, coexpression cluster id (cid)': 
                     'Gene coexpression clusters (cid)'}, inplace=True)
new_df.loc[new_df['ID'].str.startswith('cid_cluster_id'), 'Description'] = 'Cluster id'
new_df.rename(index={'Network clusters': 
                     'Gene coexpression network features (coe)'}, inplace=True)
new_df.loc[new_df['ID'] == 'coe_cluster_size', 'Description'] = 'Cluster size'
temp = new_df.reset_index()  # Helps to find position below
new_df.index.values[3335] = 'Gene coexpression network features (coe)'
new_df.index.values[3336] = 'Gene coexpression network features (coe)'
new_df.index.values[3334] = 'Gene coexpression network features (coe)'
new_df.loc[new_df['ID'] == 'coe_deg_cen', 'Description'] = 'Node degree'
new_df.loc[new_df['ID'] == 'coe_bet_cen', 'Description'] = 'Node betweeness centrality'

# PPI features
new_df.rename(index={'Network centrality': 
                     'Protein protein interaction, PPI network features (ppi)'}, inplace=True)
new_df.loc[new_df['ID'] == 'ppi_deg_cen', 'Description'] = 'Node degree'
new_df.loc[new_df['ID'] == 'ppi_bet_cen', 'Description'] = 'Node betweeness centrality'

new_df.to_csv(OUTPUT, sep='\t')
