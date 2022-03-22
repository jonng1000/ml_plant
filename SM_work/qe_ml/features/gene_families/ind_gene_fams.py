# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:22:41 2019

@author: weixiong001

Mann Whitney U test to see if gene family size differs between GM and
SM genes.

Creates gene_families.txt file, which has the gene family size feature.
"""

import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

orthogrps_df = pd.read_csv('./OF_linux190919/Orthogroups.tsv',
                           sep='\t', index_col=0)

# Selecting Arabidopsis orthogroups, where each Orthogroup is an index,
#and the value in each othogroup is one string, containing all the genes
#in the group, hence further downstream processing is needed
ath = orthogrps_df['ath_modified']

ath_orthogrps = {}
for items in ath.iteritems(): 
    orthogroup = items[0]
    unprocessed_genes = items[1]
    # Deals with nan since not all orthogroups have genes for a specific
    # species
    if type(unprocessed_genes) == float:
        continue
    else:
        # Splits long string into a list of sublists, where each sublist is 
        # a gene with its long ID
        ug_split = unprocessed_genes.split(', ')
        # Splits each long gene ID and selects the ID which is a whole number,
        # as the gene's ID
        ug_split_split = [item.split('|')[1] for item in ug_split]
        # Converts the list of gene IDs (corrected) into a set for easy
        # membership testing
        ug_ss_set = set(ug_split_split)
        # Data checking
        if len(ug_ss_set) != len(ug_split_split):
            print('Error, duplicate genes')
            break
        
        for gene in ug_ss_set:
            # Data checking
            if gene in ath_orthogrps:
                print('Error, gene already present')
                break
            else:
                # Builds dict where each orthogroup is a key, and the value is
                # the set of all gene IDs in it
                ath_orthogrps[gene] = len(ug_ss_set)

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

ath_df = pd.DataFrame.from_dict(ath_orthogrps,
                                orient='index', columns=['OG_size'])
ath_df['Category'] = np.nan
m1 = ath_df.index.isin(priGO)
m2 = ath_df.index.isin(secGO)
ath_df['Category'] = ath_df['Category'].mask(m1, 'GM')
ath_df['Category'] = ath_df['Category'].mask(m2, 'SM')

ath_df.to_csv('gene_families.txt', sep='\t')
##############################################################################
# This is to see the differences in gene family size between GM and SM genes
# Performing data analysis and plotting
ax = sns.violinplot(x='Category', y='OG_size', data=ath_df)
plt.figure()

ax = sns.boxplot(x='Category', y='OG_size', data=ath_df)
plt.figure()
ax = sns.boxplot(x='Category', y='OG_size', data=ath_df, showfliers=False)
plt.figure()

GM = ath_df[ath_df['Category']=='GM']
SM = ath_df[ath_df['Category']=='SM']
ax = sns.distplot(GM['OG_size'], kde=False)
ax.set_xlabel('GM OG_size')
plt.savefig("GM_OG.svg")
plt.figure()
ax = sns.distplot(SM['OG_size'], kde=False)
ax.set_xlabel('SM OG_size')
plt.savefig("SM_OG.svg")
plt.figure()

# MannwhitneyuResult(statistic=44738.0, pvalue=6.193629678157233e-18)
mannwhitneyu(GM['OG_size'], SM['OG_size'])
# MannwhitneyuResult(statistic=44738.0, pvalue=1.2387259356314466e-17)
mannwhitneyu(GM['OG_size'], SM['OG_size'], alternative='two-sided')
# MannwhitneyuResult(statistic=44738.0, pvalue=6.193629678157233e-18)
mannwhitneyu(GM['OG_size'], SM['OG_size'], alternative='less')
# MannwhitneyuResult(statistic=44738.0, pvalue=1.0)
mannwhitneyu(GM['OG_size'], SM['OG_size'], alternative='greater')
# MannwhitneyuResult(statistic=124210.0, pvalue=6.193629678157233e-18)
mannwhitneyu(SM['OG_size'], GM['OG_size'], alternative='greater')
##############################################################################      

##############################################################################
# replacing na values with no_label, as nan values cannot be used for plotting
ath_df['Category'].fillna('no_label', inplace = True)
no_label = ath_df[ath_df['Category']=='no_label']
ax = sns.distplot(no_label['OG_size'], kde=False)
ax.set_xlabel('no_label OG_size')
plt.savefig("nl_OG.svg")
plt.figure()
ax = sns.boxplot(x='Category', y='OG_size', data=ath_df)
plt.savefig("OG_boxplot_out.svg")
plt.figure()
ax = sns.boxplot(x='Category', y='OG_size', data=ath_df, showfliers=False)
plt.savefig("OG_boxplot.svg")
plt.figure()
ax = sns.violinplot(x='Category', y='OG_size', data=ath_df)
plt.figure()

no_label.describe()
#no_label.describe()
#Out[46]: 
#            OG_size
#count  24178.000000
#mean       8.963686
#std       16.545925
#min        1.000000
#25%        1.000000
#50%        3.000000
#75%        9.000000
#max      120.000000

SM.describe()
#SM.describe()
#Out[48]: 
#          OG_size
#count  114.000000
#mean    12.201754
#std     13.670704
#min      1.000000
#25%      3.000000
#50%      8.000000
#75%     16.000000
#max     88.000000

# MannwhitneyuResult(statistic=924972.0, pvalue=8.215619651468886e-10)
mannwhitneyu(no_label['OG_size'], SM['OG_size'], alternative='two-sided')
