# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:31:25 2021

@author: weixiong001

Analyse results from ml workflow, plots results, but modifed to have error bars,
for publication
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'compiled_times.txt'
FIG = 'go_class_time.png'
FIG2 = 'all_time.png'

data = pd.read_csv(FILE, sep='\t', index_col=0)

fig, ax = plt.subplots(figsize=(15, 5))
ax.set(yscale='log')
sns.barplot(data=selected, x='GO_class', y='time_taken_(s)', hue='model_name',
            ax=ax)
# add the annotation for mean
for i in ax.containers:
    ax.bar_label(i, fmt='Mean:\n%.1f',  label_type='edge')
plt.savefig(FIG)
plt.close()

fig, ax = plt.subplots()
ax.set(yscale='log')
sns.barplot(data=selected, x='model_name', y='time_taken_(s)', ax=ax)
for i in ax.containers:
    ax.bar_label(i, fmt='Mean:\n%.1f',  label_type='edge')
plt.savefig(FIG2)
plt.close()
