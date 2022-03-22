# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 14:29:43 2021

@author: weixiong001

Create feature category info file
"""

import pandas as pd
import csv
FILE = 'dump.data.mci.I20'
FILE2 = 'D:/GoogleDrive/machine_learning/ml_scores_overall/go_scores_domains.txt'
FILE3 = 'D:/GoogleDrive/machine_learning/ml_scores_overall/dge_scores_groups.txt'
OUTPUT = 'feat_cat_info.txt'

# Open files
with open(FILE, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    cluster_dict = {}
    cluster_id = 0
    for row in csv_reader:
        cluster_id += 1
        cluster_size = len(row)
        for gene in row:
            if gene not in cluster_dict:
                cluster_dict[gene] = [cluster_id, cluster_size]
            else:
                print(gene, 'already present!')

df = pd.DataFrame.from_dict(cluster_dict, orient='index')
df.index.name = 'Feature'
df = df.rename(columns={0: 'feat_cluster_id', 1: 'feat_cluster_size'})
filtered = df.loc[df['feat_cluster_size'] > 2, :]

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
for feature in filtered.index:
    prefix = feature.split('_')[0] + '_'
    if prefix == 'dge_' or prefix == 'go_':
        continue
    else:
        other_feat[feature] = map_dict[prefix]
features_series = pd.Series(other_feat)

# Assign categories to features in clusters
all_categories = pd.concat([go_domains, dge_cat, features_series])
fc_cat_df = pd.concat([filtered, all_categories], axis=1, join='inner')
fc_cat_df.rename(columns={0: 'feat_category'}, inplace=True)
fc_cat_df.index.name = 'feature'
'''
# 36 feature categories
len(set(fc_cat_df['feat_category']))
Out[114]: 36
'''

fc_cat_df.to_csv(OUTPUT, sep='\t')
