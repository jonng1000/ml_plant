# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:03:42 2021

@author: weixiong001

Plots simpler barplot
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

FILE = 'pvalue_corrected.txt'
FILE2 = 'feat_cat_info.txt'
FIG = 'baplot_explore.png'
FIG2 = 'focused_baplot_explore.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

# Creating mapper to rename columns (feature cluster ids)
temp_df = df2.loc[:, ['feat_cluster_id', 'feat_cluster_size']].drop_duplicates()
temp_df = temp_df.set_index('feat_cluster_id')
# Use stable sort as cluster ids are in order so want to preserve this
temp_df.sort_values('feat_cluster_size', kind='stable', ascending=False, inplace=True)
cluster_size = '(' + temp_df['feat_cluster_size'].astype(str) + ')'
cluster_names = temp_df.index.astype(str) + '_' + cluster_size
cluster_names.index = cluster_names.index.astype(str)
cluster_names_map = cluster_names.to_dict()
# Creating mapper to rename index (feature categories)
feat_cat = df2.groupby('feat_category').size().sort_values(ascending=False)
feat_cat_names = feat_cat.index + '_(' + feat_cat.astype(str) + ')'
feat_cat_names_map = feat_cat_names.to_dict()

rename_df = df.rename(columns=cluster_names_map)
rename_df = rename_df.rename(index=feat_cat_names_map)
rename_df = rename_df.loc[feat_cat_names, :]

counts_1 = (rename_df == 1).sum()
counts_1.name = 'Freq'
counts_1.index.name = 'Feat_cluster_ID'

plt.figure(figsize=(15,7))
g = sns.barplot(x=counts_1.index, y=counts_1, orient='v')
g.set_xticklabels(g.get_xticklabels(), rotation=90)
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()


#plt.figure(figsize=(15,7))
g2 = sns.barplot(x=counts_1.iloc[:20].index, y=counts_1.iloc[:20], orient='v')
g2.set_xticklabels(g2.get_xticklabels(), rotation=90)
plt.tight_layout()
g2.figure.savefig(FIG2)
plt.close()



