# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:03:42 2021

@author: weixiong001

Plots clustermap, statistically significant enriched/depleted 
number of edges across feature categories
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'pvalue_corrected.txt'
FILE2 = 'feature_category_info.txt'
FIG = 'clustermap_sig.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
'''
# 663 feature categories
len(df)
Out[259]: 663
'''

invert_df = df.loc[:, ['category_2', 'category_1', 'corrected_result']]
invert_df.rename(columns={'category_2': 'category_1', 'category_1': 'category_2'}, inplace=True)
combined_2dfs = pd.concat([df, invert_df])
rem_duplicates = combined_2dfs.drop_duplicates()
'''
# 4 combinations arent present
len(rem_duplicates)
Out[45]: 1292
36*36 -> because heatmap generated has 36 x 36 categories
Out[43]: 1296
'''
temp = rem_duplicates.set_index(['category_1', 'category_2'])
unstacked = temp.unstack()
unstacked.columns = unstacked.columns.get_level_values(1)
unstacked.columns.name = None
unstacked.index.name = 'feature_category'

# Creating mapper to rename feature categories
feat_cat_size = df2.groupby('feat_category').size()
sorted_categories = feat_cat_size.sort_values(ascending=False)
new_names = sorted_categories.index + '_(' + sorted_categories.astype(str) + ')'
new_names_map = new_names.to_dict()
# Renaming dataframe
rename_df = unstacked.rename(columns=new_names_map)
rename_df = rename_df.rename(index=new_names_map)
'''
# 2 (4 due to symmetry of columns) category pairs are na as it doesnt exist,
# to see which ones, need to look at heatmap, replace them with 0
rename_df.isna().sum().sum()
Out[82]: 4
'''
rename_df.fillna(0, inplace=True)
"""
# Obtained from calling new_names.values
# Order names by grouping them according to their relatedness to each other
ordered_names = ['Coexp clusters_(248)', 'Coexp network features_(1)', 
                 'Aranet clusters_(245)', 'Aranet network features_(1)',
                 'PPI clusters_(77)', 'PPI network features_(1)',
                 'Pfam domains_(33)', 'Disordered domains regions_(1)',
                 'Transmembrane helices_(1)', 'Number of domains_(2)',
                 'Protein PTMs_(7)', 'Biochemical features_(2)',
                 'Regulatory clusters_(38)', 'Regulatory network features_(1)',
                 'TF-TG properties_(37)', 'cis-regulatory element names_(36)', 
                 'cis-regulatory element families_(15)', 
                 'GO_biological_process_(236)', 'GO_molecular_function_(74)',
                 'GO_cellular_component_(48)', 'DGE_stress and stimulus_(50)',
                 'DGE_general molecular function_(44)',
                 'DGE_growth and development_(38)', 
                 'DGE_infection and immunity_(31)', 
                 'DGE_light and circadian_(16)', 'Homolog features_(22)',
                 'Orthogroups_(2)', 'Phylostrata_(1)', 
                 'Conservation features_(5)', 'Single copy_(1)',
                 'Tandemly duplicated_(1)', 'Diurnal timepoints_(12)',
                 'TWAS features_(8)', 'TPM features_(5)', 'SPM features_(1)',        
                 'Gene body methlyated_(1)']
"""
#rename_df = rename_df.loc[ordered_names, ordered_names]

plt.figure(figsize=(13,10))
# Default location of cbar ticks [-1, 0, 1] cbar_kws={'ticks':[-0.667, 0, 0.667], 'label': ['Depleted', 'No significance', 'Enriched']}
g = sns.clustermap(rename_df, cmap=sns.diverging_palette(240, 10, n=3, center='dark'))
g_colorbar =g.ax_heatmap.collections[0].colorbar
#g_colorbar.set_ticks([-1, 0, 1])  # Orig cbar ticks position
g_colorbar.set_ticks([-0.667, 0, 0.667])
g_colorbar.set_ticklabels(['Depleted', 'No significance', 'Enriched'])

plt.tight_layout()
g.savefig(FIG)
plt.close()
