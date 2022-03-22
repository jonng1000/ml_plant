# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 19:00:22 2019

@author: weixiong001
"""
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('procesed_ratios_lca.txt', sep='\t', index_col=0, 
                 header=[0,1])

only_divided_ratios = df[[i for i in df.columns if 'divided' in i[1]]]
#plt.figure()
#plt.figure(figsize=(20, 15))
#ax = sns.boxplot(data=only_divided_ratios)

# Why does this not work??
#incorrect_long_ratios = only_divided_ratios.stack([0, 1]).reset_index()

long_ratios = pd.melt(only_divided_ratios, value_vars=only_divided_ratios.columns.tolist())
plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=long_ratios)
plt.savefig('ratios_w_outliers.png')
plt.figure()
plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=long_ratios, showfliers=False)
plt.savefig('ratios_no_outliers.png')
only_log2_ratios = df[[i for i in df.columns if 'log2' in i[1]]]
log2_ratios = pd.melt(only_log2_ratios, value_vars=only_log2_ratios.columns.tolist())

plt.figure()
plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=log2_ratios)
plt.savefig('log2_ratios_w_outliers.png')
plt.figure()
plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=log2_ratios, showfliers=False)
plt.savefig('log2_ratios_no_outliers.png')

#plt.figure()
#transposed_divided_ratios = only_divided_ratios.T
#ax = transposed_divided_ratios.plot(kind='bar', fontsize=16, figsize=(24, 18))
#ax.legend(markerscale=4, fontsize=16)
#plt.savefig('test2.png')


# Do not do this, not sure what it does, but it probably plots 10 000
# individual plots, and takes quite long. Second code block also takes long,
# stopped it halfway but it may do the same thing as the first block
#plt.figure()
#ax = only_divided_ratios.plot(kind='bar', fontsize=16, figsize=(24, 18))
#ax.legend(markerscale=4, fontsize=16)
#plt.figure()
#transposed_divided_ratios = only_divided_ratios.T
#ax = transposed_divided_ratios.plot(kind='bar', fontsize=16, figsize=(24, 18))
#ax.legend(markerscale=4, fontsize=16)
#plt.savefig('test2.png')
