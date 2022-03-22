# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:25:58 2020

@author: weixiong001

Sort and print number of genes in each GO class. Plotted graphs, but it isn't
necessary
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('GO_gene_counts.txt', sep='\t', index_col=0)
sorted_df = df.sort_values(by='Counts', ascending=False)
sorted_df.to_csv('sort_GO_gene_counts.txt', sep='\t')

# Plotted graph of all GO gene counts, but graph becomes small due to
# extreme values, also takes a long time to load, so can skip this
# ax = sns.barplot(x=sorted_df.index, y='Counts', ci=None, data=sorted_df)
# ax.set(xticklabels=[])
# ax.set(xticks=[])

filtered = sorted_df[sorted_df['Counts'] >= 500]
ax = sns.barplot(x=filtered.index, y='Counts', ci=None, data=filtered)
ax.set(xticklabels=[])
ax.set(xticks=[])

