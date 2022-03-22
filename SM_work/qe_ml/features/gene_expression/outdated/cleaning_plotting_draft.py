# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:44:22 2019

@author: weixiong001
"""

import pandas as pd
import numpy as np
import csv
import seaborn as sns

with open('selected_sra.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    selected = {row[0]:row[1] for row in reader}

selected_cols = ['gene'] + list(selected.keys())
df = pd.read_csv('Ath_matrix.txt', sep='\t', index_col=0, usecols=selected_cols)

renamed_df = df.rename(columns=selected)
renamed_df.columns.name = 'Tissue'
transposed = renamed_df.T.reset_index()

mean_gene_ex = transposed.groupby(['Tissue']).mean().T
mean_gene_ex = mean_gene_ex.rename(columns={x:'mean_' + x for x in mean_gene_ex.columns})
median_gene_ex = transposed.groupby(['Tissue']).median().T
median_gene_ex = median_gene_ex.rename(columns={x:'median_' + x for x in median_gene_ex.columns})
max_gene_ex = transposed.groupby(['Tissue']).max().T
max_gene_ex = max_gene_ex.rename(columns={x:'max_' + x for x in max_gene_ex.columns})
min_gene_ex = transposed.groupby(['Tissue']).min().T
min_gene_ex = min_gene_ex.rename(columns={x:'min_' + x for x in min_gene_ex.columns})

gene_ex_df = pd.concat([mean_gene_ex, median_gene_ex, max_gene_ex, 
                        min_gene_ex], axis=1)

# These Arabidopsis GO terms have already been filtered to only include
# experimental evidence codes
parent_folder = r'D:/GoogleDrive/machine learning/getting_targets'
with open(parent_folder + r'/GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        priGO = row
with open(parent_folder + r'/GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        secGO = row

# Labelling the genes with each category : SM/GM/no_label        
gene_ex_df['Category'] = np.nan
m1 = gene_ex_df.index.isin(priGO)
m2 = gene_ex_df.index.isin(secGO)
gene_ex_df['Category'] = gene_ex_df['Category'].mask(m1, 'GM')
gene_ex_df['Category'] = gene_ex_df['Category'].mask(m2, 'SM')
gene_ex_df['Category'].fillna('no_label', inplace = True)

tests_df = gene_ex_df[[x for x in gene_ex_df.columns if 'mean' in x] + ['Category']]
%matplotlib inline
%matplotlib qt
boxplot = tests_df.boxplot(figsize=(20,15), by='Category', showfliers=False)

