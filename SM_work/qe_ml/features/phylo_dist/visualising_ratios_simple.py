# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:54:20 2019

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv('genes_lca.txt', sep='\t', index_col=0)

ax = sns.countplot(x='Category', hue='taxon', data=df)
ax.axes.set_yscale('log')

counts = df.groupby('Category')['taxon'].value_counts()
counts.to_csv('test_counts.tsv', sep='\t')
total = df.groupby('Category')['taxon'].value_counts().sum()
percent = 100*counts/total
percent.name = 'percent'
new_percent = percent.reset_index()
plt.figure()
ax = sns.barplot(x='Category', hue='taxon', y='percent', data=new_percent)
ax.axes.set_yscale('log')
#percent.plot(kind='bar')

counts.name = 'counts'
percent_GMSMnl = counts.groupby(level=0).apply(lambda x: 100 * x/x.sum())
new_percent_GMSMnl = percent_GMSMnl.reset_index()
new_percent_GMSMnl.rename(columns={'counts':'percent'}, inplace=True)
plt.figure()
ax = sns.barplot(x='Category', hue='taxon', y='percent', data=new_percent_GMSMnl)
plt.savefig('genes_percent_within_cat.png')

proportion_GMSMnl = counts.groupby(level=0).apply(lambda x: x/x.sum())
new_prop_GMSMnl = proportion_GMSMnl.reset_index()
new_prop_GMSMnl.rename(columns={'counts':'ratio'}, inplace=True)
plt.figure()
ax = sns.barplot(x='Category', hue='taxon', y='ratio', data=new_prop_GMSMnl)
ax.set_ylabel('proportion')
plt.savefig('genes_prop_within_cat.png')
plt.figure()
ax = sns.barplot(x='Category', hue='taxon', 
                 hue_order=['eudicot', 'angiosperm',
                            'embryophyte', 'viridiplantae'],
                 y='ratio', data=new_prop_GMSMnl
                 )
ax.set_ylabel('proportion')
plt.savefig('genes_prop_within_cat.svg')