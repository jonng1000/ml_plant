# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:35:55 2021

@author: weixiong001

Plot heatmap of categorical features, normalised counts by converting it to
proportions
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'go_scores.txt'
FILE2 = 'edited_catf_scores.txt'
FILE3 = 'dge_scores.txt'
FIG = 'heatmap_catf.png'

def sel_bins(a_df, feat_cat):
    fc = a_df.loc[a_df.index.str.startswith(feat_cat + '_')]
    fc_bins = fc.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                    0.8, 0.9, 1], normalize=True)
    fc_bins.name = feat_cat
    return fc_bins


df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 =  pd.read_csv(FILE2, sep='\t', index_col=0)
df3 = pd.read_csv(FILE3, sep='\t', index_col=0)

go = df.loc[:, 'oob_f1']
go_bins = go.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                0.8, 0.9, 1], normalize=True)
go_bins.name = 'GO terms'

dge = df3.loc[:, 'oob_f1']
dge_bins = dge.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                  0.8, 0.9, 1], normalize=True)
dge_bins.name = 'DGE'

selected = df2.loc[:, 'oob_f1']

pid_bins = sel_bins(selected, 'pid')
agi_bins = sel_bins(selected, 'agi')
cid_bins = sel_bins(selected, 'cid')
tti_bins = sel_bins(selected, 'tti')
hom_bins = sel_bins(selected, 'hom')
dit_bins = sel_bins(selected, 'dit')
# These feature categories have <10 features
sin_bins = sel_bins(selected, 'sin')
tan_bins = sel_bins(selected, 'tan')
gbm_bins = sel_bins(selected, 'gbm')

temp = pd.concat([go_bins, pid_bins, agi_bins, dge_bins, cid_bins,
                  tti_bins, hom_bins, dit_bins, sin_bins, tan_bins,
                  gbm_bins], axis=1)
temp = temp.transpose()
plt.figure(figsize=(7,5))
g = sns.heatmap(temp, cmap='flare', cbar_kws={'label': 'Normalized'})
g.set(xlabel='oob_F1')
'''
# Default positions without changing xticks
g.get_xticks()
Out[322]: array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
'''
# Shift xtick positions by 0.5 to the right, add one at position 0
g.set_xticks(list(range(11)))
g.set_xticklabels([str(x/10) for x in range(11)])
g.set_yticklabels(['1379 GO terms','1294 PPI clusters','2956 Aranet clusters',
                   '436 DGEs','278 Coexp clusters', '54 Regulatory clusters',
                   '22 Homolog features','12 Diurnal timepoints', 
                   '1 Single copy', '1 Tandemly duplicated',
                   '1 Gene body methlyated'])
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()
