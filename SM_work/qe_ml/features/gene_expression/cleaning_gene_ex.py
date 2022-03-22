# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:44:22 2019

@author: weixiong001

Takes in Ath_matrix.txt (gene expression file), Ath_sampleAnnotation.txt
(maps columns to tissue names), selected_sra.txt (tissues which I want),
creates various measures of gene expression, and creates a file called
processed_gene_ex.txt. This has all the processed gene expression values.
"""

import pandas as pd
import numpy as np
import csv
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import mannwhitneyu
from scipy.stats import median_absolute_deviation

with open('selected_sra.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    selected = {row[0]:row[1] for row in reader}

selected_cols = ['gene'] + list(selected.keys())
df = pd.read_csv('Ath_matrix.txt', sep='\t', index_col=0, usecols=selected_cols)
renamed_df = df.rename(columns=selected)

mean = renamed_df.mean(axis=1)
median =  renamed_df.median(axis=1)
max_rdf =  renamed_df.max(axis=1)
min_rdf =  renamed_df.min(axis=1)
var = renamed_df.var(axis=1)
mad_var = median_absolute_deviation(renamed_df, axis=1)/median

renamed_df['mean_exp'] = mean
renamed_df['median_exp'] = median
renamed_df['max_exp'] = max_rdf
renamed_df['min_exp'] = min_rdf
renamed_df['var_exp'] = var
varlog10 = np.log10(renamed_df['var_exp'])
renamed_df['var_exp_log10'] = varlog10
renamed_df['var_median'] = mad_var

# Not sure if its needed
#lowest = np.sort(renamed_df['var_exp_log10'].unique())[1]
#renamed_df['var_exp_log10'] = renamed_df['var_exp_log10'].replace([np.inf, -np.inf], lowest)

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
renamed_df['Category'] = np.nan
m1 = renamed_df.index.isin(priGO)
m2 = renamed_df.index.isin(secGO)
renamed_df['Category'] = renamed_df['Category'].mask(m1, 'GM')
renamed_df['Category'] = renamed_df['Category'].mask(m2, 'SM')
# Filling in place doesn't work, something to do with changing values in
# a copy, probably not that impt to know
renamed_df['Category'] = renamed_df['Category'].fillna('no_label')
renamed_df.to_csv('processed_gene_ex.txt', sep='\t')

ax = sns.boxplot(x='Category', y='mean_exp', data=renamed_df)
plt.savefig('mean_outliers.png')
plt.savefig('mean_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='mean_exp', data=renamed_df, showfliers=False)
plt.savefig('mean_no_outliers.png')
plt.savefig('mean_no_outliers.svg')
mean_description = renamed_df.groupby('Category')['mean_exp'].describe()
mean_description.to_csv('mean_description.txt', sep='\t')
median_description = renamed_df.groupby('Category')['median_exp'].describe()
median_description.to_csv('median_description.txt', sep='\t')
max_description = renamed_df.groupby('Category')['max_exp'].describe()
max_description.to_csv('max_description.txt', sep='\t')
min_description = renamed_df.groupby('Category')['min_exp'].describe()
min_description.to_csv('min_description.txt', sep='\t')
var_description = renamed_df.groupby('Category')['var_exp'].describe()
var_description.to_csv('var_description.txt', sep='\t')
#mean_description
#Out[19]: 
#            count       mean         std  ...        50%        75%           max
#Category                                  ...                                    
#GM         1486.0  35.994814   99.038458  ...  12.895882  31.563289   2607.309033
#SM          115.0  44.309487   78.534017  ...  17.196205  50.981318    490.030155
#no_label  25781.0  36.515888  249.557907  ...   6.002328  19.094073  27054.002968

median_description = renamed_df.groupby('Category')['mean_exp'].describe()
#mean_description.loc[:, 'count':'25%']
#Out[25]: 
#            count       mean         std  min       25%
#Category                                               
#GM         1486.0  35.994814   99.038458  0.0  5.520567
#SM          115.0  44.309487   78.534017  0.0  3.090626
#no_label  25781.0  36.515888  249.557907  0.0  0.704510


plt.figure()
ax = sns.boxplot(x='Category', y='median_exp', data=renamed_df)
plt.savefig('median_outliers.png')
plt.savefig('median_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='median_exp', data=renamed_df, showfliers=False)
plt.savefig('median_no_outliers.png')
plt.savefig('median_no_outliers.svg')

plt.figure()
ax = sns.boxplot(x='Category', y='max_exp', data=renamed_df)
plt.savefig('max_outliers.png')
plt.savefig('max_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='max_exp', data=renamed_df, showfliers=False)
plt.savefig('max_no_outliers.png')
plt.savefig('max_no_outliers.svg')

plt.figure()
ax = sns.boxplot(x='Category', y='min_exp', data=renamed_df)
plt.savefig('min_outliers.png')
plt.savefig('min_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='min_exp', data=renamed_df, showfliers=False)
plt.savefig('min_no_outliers.png')
plt.savefig('min_no_outliers.svg')

# Below produces snslog10_no.png before -inf varience values are replaced by
# lowest varience values
#ax = sns.boxplot(x='Category', y='var_exp', data=renamed_df, showfliers=False)
#ax.set(yscale="log")
# Below produces log10_no.png before -inf varience values are replaced by
# lowest varience values
#ax = sns.boxplot(x='Category', y='var_exp_log10', data=renamed_df, showfliers=False)

plt.figure()
ax = sns.boxplot(x='Category', y='var_exp', data=renamed_df)
plt.savefig('var_outliers.png')
plt.savefig('var_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='var_exp', data=renamed_df, showfliers=False)
plt.savefig('var_no_outliers.png')
plt.savefig('var_no_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='var_exp_log10', data=renamed_df)
plt.savefig('varlog10_outliers.png')
plt.figure()
ax = sns.boxplot(x='Category', y='var_exp_log10', data=renamed_df, showfliers=False)
plt.savefig('varlog10_no_outliers.png')

plt.figure()
ax = sns.boxplot(x='Category', y='var_median', data=renamed_df)
plt.savefig('var_median_outliers.png')
plt.savefig('var_median_outliers.svg')
plt.figure()
ax = sns.boxplot(x='Category', y='var_median', data=renamed_df, showfliers=False)
plt.savefig('var_median_no_outliers.png')
plt.savefig('var_median_no_outliers.svg')

GM = renamed_df[renamed_df['Category']=='GM']
SM = renamed_df[renamed_df['Category']=='SM']
nl = renamed_df[renamed_df['Category']=='no_label']
abc
# MannwhitneyuResult(statistic=83119.5, pvalue=0.6264211770485237)
mannwhitneyu(GM['mean_exp'], SM['mean_exp'], alternative='two-sided')

# MannwhitneyuResult(statistic=1063224.5, pvalue=1.5974489924456174e-07)
mannwhitneyu(nl['mean_exp'], SM['mean_exp'], alternative='two-sided')


# MannwhitneyuResult(statistic=106724.0, pvalue=8.388247166032604e-06)
mannwhitneyu(GM['median_exp'], SM['median_exp'], alternative='two-sided')

# MannwhitneyuResult(statistic=1318436.5, pvalue=0.03914685751655136)
mannwhitneyu(nl['median_exp'], SM['median_exp'], alternative='two-sided')


# MannwhitneyuResult(statistic=71978.5, pvalue=0.0048130107991389785)
mannwhitneyu(GM['var_exp'], SM['var_exp'], alternative='two-sided')

# MannwhitneyuResult(statistic=968001.5, pvalue=1.2633992133927643e-10)
mannwhitneyu(nl['var_exp'], SM['var_exp'], alternative='two-sided')


# MannwhitneyuResult(statistic=45103.5, pvalue=2.932923075836348e-17)
mannwhitneyu(GM['var_median'], SM['var_median'], alternative='two-sided')

# MannwhitneyuResult(statistic=1423113.0, pvalue=0.4576665477937141)
mannwhitneyu(nl['var_median'], SM['var_median'], alternative='two-sided')


# MannwhitneyuResult(statistic=1740231.0, pvalue=0.00029373995839892457)
mannwhitneyu(nl['min_exp'], SM['min_exp'], alternative='two-sided')

# MannwhitneyuResult(statistic=125597.0, pvalue=1.1081810432066854e-17)
mannwhitneyu(GM['min_exp'], SM['min_exp'], alternative='two-sided')


# MannwhitneyuResult(statistic=966157.5, pvalue=1.085278657419278e-10)
mannwhitneyu(nl['max_exp'], SM['max_exp'], alternative='two-sided')

# MannwhitneyuResult(statistic=71662.5, pvalue=0.003908567246659481)
mannwhitneyu(GM['max_exp'], SM['max_exp'], alternative='two-sided')
