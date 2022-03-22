# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:31:25 2021

@author: weixiong001

Plot time taken by ml models
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'compiled_times.txt'
FIG = 'go_class_time.pdf'
FIG2 = 'all_time.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)

fig, ax = plt.subplots(figsize=(15, 5))
ax.set(yscale='log')
sns.barplot(data=df, x='GO_class', y='time_taken_(s)', hue='model_name',
            ax=ax)
# add the annotation for mean
for i in ax.containers:
    ax.bar_label(i, fmt='Mean:\n%.1f',  label_type='edge')
plt.savefig(FIG)
plt.close()

fig, ax = plt.subplots(figsize=(15, 5))
ax.set(yscale='log')
sns.barplot(data=df, x='model_name', y='time_taken_(s)', ax=ax)
for i in ax.containers:
    ax.bar_label(i, fmt='Mean:\n%.1f',  label_type='edge')
plt.savefig(FIG2)
plt.close()
