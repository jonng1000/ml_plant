# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 01:18:50 2021

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'dge_nodes_edge_counts.txt'
OUTPUT = 'sorted_dge_nodes_edges.txt'
FIG = 'dge_edge_counts.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df['diff_expt'] = df['diff_DGE_category'] + df['same_DGE_category']
# Sorted according to num of features linked to diff DGE expts
# code above shows the defn of diff DGE expts
sorted_diff_expt = df.sort_values(by=['diff_expt'], ascending=False)
sorted_diff_expt.to_csv(OUTPUT, sep='\t')

g = sns.histplot(data=df, x='diff_expt')
g.figure.savefig(FIG)
plt.close()