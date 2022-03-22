# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 14:29:43 2021

@author: weixiong001

Create feature category info file
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/fi_network/network_analysis/selected_mr.txt'
FILE2 = 'D:/GoogleDrive/machine_learning/ml_scores_overall/go_scores_domains.txt'
FILE3 = 'D:/GoogleDrive/machine_learning/ml_scores_overall/dge_scores_groups.txt'
OUTPUT = 'feature_category_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df = df.rename(columns={'f1': 'source', 'f2': 'target'})

# Get feature categories
go_df = pd.read_csv(FILE2, sep='\t', index_col=0)
go_df.index = go_df.index.str.replace('go_GO_', 'go_GO:')
go_df['GO_domain'] = 'GO_' + go_df['GO_domain'].astype(str)
go_domains = go_df.loc[:, 'GO_domain']

dge_df = pd.read_csv(FILE3, sep='\t', index_col=0)
dge_cat = dge_df.loc[:, 'Big_Cat']
dge_cat = 'DGE_' + dge_cat

# 'gbm_' is the last categorical feature, the rest are continuous
map_dict = {'pid_': 'PPI clusters', 'agi_': 'Aranet clusters', 
            'cid_': 'Coexp clusters', 'tti_': 'Regulatory clusters',
            'hom_': 'Homolog features', 'dit_': 'Diurnal timepoints', 
            'sin_': 'Single copy', 'tan_': 'Tandemly duplicated',
            'gbm_': 'Gene body methlyated',
            'pfa_': 'Pfam domains', 'cin_': 'cis-regulatory element names',
            'ptm_': 'Protein PTMs', 'ttf_': 'TF-TG properties',
            'gwa_': 'GWAS features', 'twa_': 'TWAS features',
            'cif_': 'cis-regulatory element families', 
            'con_': 'Conservation features', 'spm_': 'SPM features', 
            'tpm_': 'TPM features', 'ort_': 'Orthogroups', 'dia_': 'Diurnal amplitude',
            'phy_': 'Phylostrata', 'mob_': 'Disordered domains regions',
            'tmh_': 'Transmembrane helices', 'pep_': 'Biochemical features',
            'num_': 'Number of domains', 'ppi_': 'PPI network features',
            'coe_': 'Coexp network features', 'ttr_': 'Regulatory network features',
            'agn_': 'Aranet network features', 'ntd_': 'Nucleotide Diversity'}

other_feat = {}
feature_set = set(df['source']) | set(df['target'])
for feature in feature_set:
    prefix = feature.split('_')[0] + '_'
    if prefix == 'dge_' or prefix == 'go_':
        continue
    else:
        other_feat[feature] = map_dict[prefix]
features_series = pd.Series(other_feat)

# Assign categories to features in clusters
all_categories = pd.concat([go_domains, dge_cat, features_series])
feature_series = pd.Series(data=range(len(feature_set)), index=list(feature_set))
fc_cat_df = pd.concat([feature_series, all_categories], axis=1, join='inner')
fc_cat_df.rename(columns={1: 'feat_category'}, inplace=True)
fc_cat_df.drop(columns=[0], inplace=True)
fc_cat_df.index.name = 'feature'
'''
# 36 feature categories
len(set(fc_cat_df['feat_category']))
Out[114]: 36
'''

fc_cat_df.to_csv(OUTPUT, sep='\t')
