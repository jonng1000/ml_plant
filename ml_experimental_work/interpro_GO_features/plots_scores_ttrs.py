# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise F1 scores. Time trial with
10 random search iterations
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'combined_scores_ttrs.txt'
FIG = 'scores_ttrs.png'

# GO file
scores_df = pd.read_csv(FILE, sep='\t', index_col=0)

# Long form for seaborn
melted = pd.melt(scores_df, id_vars=['class_label', 'model_name'],
                 value_vars=['f1'])

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(data=melted, x='class_label', y='value', hue='model_name')
ax.xaxis.set_tick_params(rotation=90, labelsize=12)
ax.set_xlabel('Class_label', fontsize=12)
ax.set_ylabel('F1', fontsize=12)
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig(FIG)
plt.close()


'''
melted.groupby('model_name').mean()
Out[2]: 
               value
model_name          
ada         0.184166
gbc         0.194307
logr        0.395196
lsv         0.394068
rf          0.405680
xgc         0.240636
'''