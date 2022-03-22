# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:15:12 2019

@author: weixiong001

This script assembles the  machine learning features and targets, and
produces combined_data_ML.csv.
"""

import pandas as pd
import csv
import numpy as np

feature_path = r"D:\GoogleDrive\machine learning\features"

single_copy = pd.read_csv(feature_path + r"\single_copies\singe_copy_GMSM.txt", 
                           sep="\t", index_col=0)
tam_dup = pd.read_csv(feature_path + r"\tandem_duplicated\genes_tandem_dup.csv",
                      sep="\t", index_col=0)
lca = pd.read_csv(feature_path + r"\phylo_dist\genes_lca.txt", sep="\t", 
                  index_col=0)
gene_family = pd.read_csv(feature_path + r"\gene_families\gene_families.txt",
                          sep="\t", index_col=0)
gene_ex = pd.read_csv(feature_path + r"\gene_expression\processed_gene_ex.txt",
                      sep="\t", index_col=0)

new_names = []
for string in sorted(gene_ex.columns):
    string = string.replace('(','')
    string = string.replace(')','')
    string = string.replace(' ','_')
    string = string.replace(',','')
    new_names.append(string)
    
for_map = dict(zip(sorted(gene_ex.columns), new_names))
renamed_gene_ex =gene_ex.rename(columns=for_map)

ex_features = ['mean_exp', 'median_exp', 'max_exp', 'min_exp', 'var_exp',
               'var_median']
selected_ex_features = renamed_gene_ex[ex_features]
gene_family_f = gene_family['OG_size']
lca_f = lca['taxon']
single_copy_f = single_copy['single_copy']
tam_dup_f = tam_dup['tandem_dup']

data_ML = pd.concat([selected_ex_features, gene_family_f, lca_f, 
                     single_copy_f, tam_dup_f], sort=False, axis=1)

# These Arabidopsis GO terms have already been filtered to only include
# experimental evidence codes
# Copied from comparing_GMSM_tandem.py in D:\GoogleDrive\machine learning\
# data_sets_JN\features\tandem_duplicated
parent_folder = r'D:\GoogleDrive\machine learning\getting_targets'
with open(parent_folder + r'\GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        priGO = set(row)  # both set and list has same number of genes
with open(parent_folder + r'\GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        secGO = set(row)  # both set and list has same number of genes
        
data_ML['Category'] = np.nan
m1 = data_ML.index.isin(priGO)
m2 = data_ML.index.isin(secGO)
data_ML['Category'] = data_ML['Category'].mask(m1, 'GM')
data_ML['Category'] = data_ML['Category'].mask(m2, 'SM')
data_ML['Category'].fillna('no_label', inplace = True)
data_ML.index.name = 'Genes'

data_ML.to_csv('combined_data_ML.csv', sep='\t')
