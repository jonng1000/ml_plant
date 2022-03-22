# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:35:55 2021

@author: weixiong001

Generate heatmap of scores
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'go_scores.txt'
FILE2 = 'edited_catf_scores.txt'
FILE3 = 'dge_scores.txt'
FIG = 'test_heatmap.png'

def sel_bins(a_df, feat_cat):
    fc = a_df.loc[a_df.index.str.startswith(feat_cat + '_')]
    fc_bins = fc.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                    0.8, 0.9, 1])
    fc_bins.name = feat_cat
    return fc_bins


df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 =  pd.read_csv(FILE2, sep='\t', index_col=0)
df3 = pd.read_csv(FILE3, sep='\t', index_col=0)

go = df.loc[:, 'oob_f1']
go_bins = go.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                0.8, 0.9, 1])
go_bins.name = 'GO terms'

dge = df3.loc[:, 'oob_f1']
dge_bins = dge.value_counts(bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                  0.8, 0.9, 1])
dge_bins.name = 'DGE'

selected = df2.loc[:, 'oob_f1']

pid_bins = sel_bins(selected, 'pid')
agi_bins = sel_bins(selected, 'agi')
cid_bins = sel_bins(selected, 'cid')
tti_bins = sel_bins(selected, 'tti')


temp = pd.concat([go_bins, pid_bins, agi_bins, dge_bins, cid_bins,
                  tti_bins], axis=1)
temp = temp.transpose()
plt.figure()
g = sns.heatmap(temp, cmap='flare', cbar_kws={'label': 'Counts'})
g.set(xlabel='oob_F1')
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()
