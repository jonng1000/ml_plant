# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 19:21:11 2022

@author: weixiong001

Processes my feature data so that it has good values for category, name and
description columns

For use for global (all feature table) and local (local network) feature table
"""

import pandas as pd

# All 5k+ GO terms in my features
FILE = 'G:/My Drive/machine_learning/GO_labels/GO_info_network.txt'
# DGE experiments with specific names
FILE2 = 'DGE_names_status_edited.txt'
# DGE experiments with DGE categories
FILE2B = 'G:/My Drive/machine_learning/ml_scores_overall/dge_scores_groups.txt'
# Partially processed data
FILE3 = 'partial_stage1.txt'
# Final processed data
OUTPUT = 'processed_stage2.txt'

df = pd.read_csv(FILE, sep='\t')
df2 = pd.read_csv(FILE2, index_col=0, sep='\t')
df2b = pd.read_csv(FILE2B, index_col=0, sep='\t')
df3 = pd.read_csv(FILE3, sep='\t', index_col=0).reset_index()

df['GO_domain'] = df['GO_domain'].str.replace('biological_process','GO_BP terms, experimental annotation (go)')
df['GO_domain'] = df['GO_domain'].str.replace('molecular_function','GO_MF terms, experimental annotation (go)')
df['GO_domain'] = df['GO_domain'].str.replace('cellular_component','GO_CC terms, experimental annotation (go)')
df['GO_info'] = df['GO_info'].str.replace('GO_biological_process','GO_BP')
df['GO_info'] = df['GO_info'].str.replace('GO_molecular_function','GO_MF')
df['GO_info'] = df['GO_info'].str.replace('GO_cellular_component','GO_CC')
mod_df = df.set_index('GO_class')
mod_df.rename(columns={'GO_info': 'Description', 'GO_domain':'Category'}, inplace=True)
mod_df.drop(columns=['GO_desc'], inplace=True)

df2.set_index('Experiment')
mod_df2 = df2.set_index('Experiment').drop(columns=['Category', 'Specific_name', 'up_down'])
combined_draft = pd.concat([mod_df2, df2b], axis=1, join='inner')
combined_draft = combined_draft.reset_index().drop(columns=['Category', 'oob_f1'])
combined_draft.rename(columns={'index': 'DGE_feat'}, inplace=True)
combined_draft['Big_Cat'] = 'DGE_' + combined_draft['Big_Cat'].astype(str) + ' (dge)'
combined_df2 = combined_draft.set_index('DGE_feat')
combined_df2.rename(columns={'expt_name': 'Description', 'Big_Cat':'Category'}, inplace=True)

mod_df3 = df3.set_index('Feature name')
mod_df3.update(mod_df)
mod_df3.update(combined_df2)
final_df = mod_df3.reset_index()
final_df = final_df.set_index('Category')
final_df['Feature name'] = final_df['Feature name'].str.replace('dge_', '')
final_df['Feature name'] = final_df['Feature name'].str.replace('go_', '')

final_df.to_csv(OUTPUT, sep='\t')