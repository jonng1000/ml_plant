# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:26:40 2019

@author: weixiong001


"""

import pandas as pd
import seaborn as sns
import csv
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv('genes_LCA.tsv', sep='\t', index_col=0)

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
        
df['Category'] = np.nan
m1 = df.index.isin(priGO)
m2 = df.index.isin(secGO)
df['Category'] = df['Category'].mask(m1, 'GM')
df['Category'] = df['Category'].mask(m2, 'SM')
df['Category'].fillna('no_label', inplace = True)

# Groupby GM/SM/no_label, then use .agg() to apply my function to each column
# Produces counts, which is a df
counts = df.groupby('Category').agg({i:'value_counts' for i in df.columns[:-1]})
counts.fillna(0, inplace=True)
counts.index.names = ['Category','Y_or_N']

# Plots with everything (genes with 0 and 1). But actually just need genes with
# 1, as that indicates that the gene falls under that particular taxon. So
# This section is fyi

# To see how the dataframe looks like
#counts.head()
#Out[177]: 
#                 monocot  eudicot  ...  chlorophyte  viridiplantae
#Category Y_or_N                    ...                            
#GM       0        1482.0     1464  ...       1482.0            400
#         1           0.0       18  ...          0.0           1082
#SM       0         114.0      108  ...        114.0             49
#         1           0.0        6  ...          0.0             65
#no_label 0       24178.0    20874  ...      24178.0          12855

'''
ax = counts.plot(kind='bar', fontsize=16, figsize=(24, 18))
ax.legend(markerscale=4, fontsize=16)
plt.savefig('all_gene_cat.png')

wo_nolabels = counts.loc[['GM', 'SM']]
plt.figure()
ax = wo_nolabels.plot(kind='bar', fontsize=16, figsize=(24, 18))
ax.legend(markerscale=4, fontsize=16)
plt.savefig('only_GMSM_gene_cat.png')

percent_counts = 100*counts/counts.sum()
plt.figure()
ax = percent_counts.plot(kind='bar', fontsize=16, figsize=(24, 18))
ax.legend(markerscale=4, fontsize=16)
plt.savefig('percent_all_gene_cat.png')

percent_wo_nolabels = percent_counts.loc[['GM', 'SM']]
plt.figure()
ax = percent_wo_nolabels.plot(kind='bar', fontsize=16, figsize=(24, 18))
ax.legend(markerscale=4, fontsize=16)
plt.savefig('percent_only_GMSM_gene_cat.png')

percent_cat = counts.groupby(level=0).apply(lambda x: 100 * x/x.sum())
plt.figure()
ax = percent_cat.plot(kind='bar', fontsize=16, figsize=(24, 18))
ax.legend(markerscale=4, fontsize=16)
plt.savefig('percent_cat.png')
'''
abc
only_genes_1 = counts.loc[[('GM', 1), ('SM', 1), ('no_label', 1)]]

plt.figure()
ax = only_genes_1.plot(kind='bar')
plt.savefig('only_genes_1.png')

plt.figure()
ax = only_genes_1.loc[[('GM', 1), ('SM', 1)]].plot(kind='bar')
plt.savefig('only_genes_1_GMSM.png')

plt.figure()
percent_only_genes_1 = 100 * only_genes_1/only_genes_1.sum().sum()
ax = percent_only_genes_1.plot(kind='bar')
plt.savefig('only_genes_1_percent.png')

plt.figure()
ax = percent_only_genes_1.loc[[('GM', 1), ('SM', 1)]].plot(kind='bar')
plt.savefig('only_genes_1_percent_GMSM.png')