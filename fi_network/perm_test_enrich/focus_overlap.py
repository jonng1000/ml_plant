# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 16:11:50 2021

@author: weixiong001

Plots simplified heatmap
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

FILE = 'pvalue_corrected.txt'
FILE2 = 'feat_cat_info.txt'
FIG = 'overlap_heatmap.png'

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

selected = rename_df.loc[:, ['4_(39)', '7_(31)', '9_(28)']]

bool_sel = (selected['4_(39)'] == 1) | (selected['7_(31)'] == 1) | (selected['9_(28)'] == 1)
overlapping = selected.loc[bool_sel]

plt.figure(figsize=(11, 6))
g = sns.heatmap(overlapping, cmap=sns.diverging_palette(240, 10, n=3))
g_colorbar = g.collections[0].colorbar
#g_colorbar.set_ticks([-1, 0, 1])  # Orig cbar ticks position
g_colorbar.set_ticks([-0.667, 0, 0.667])
g_colorbar.set_ticklabels(['Depleted', 'No significance', 'Enriched'])
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()

