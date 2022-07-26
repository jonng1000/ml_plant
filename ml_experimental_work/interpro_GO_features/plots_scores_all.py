# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise F1 scores. 
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'combined_scores_all.txt'
FIG = 'scores_all.png'

# GO file
scores_df = pd.read_csv(FILE, sep='\t', index_col=0)

# Long form for seaborn
melted = pd.melt(scores_df, id_vars=['class_label', 'feature_type'],
                 value_vars=['oob_f1'])

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=melted, y='value')
ax.xaxis.set_tick_params(rotation=90, labelsize=12)
ax.set_xlabel('Class_label', fontsize=12)
ax.set_ylabel('F1', fontsize=12)
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig(FIG)
plt.close()


