# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:54:09 2019

@author: weixiong001

Plots feature importance
"""

import pandas as pd
import math
import seaborn as sns
from matplotlib import pyplot as plt

box_num = 100

df = pd.read_csv("feat_impt_orig.txt", sep="\t", index_col=0)
df['mean'] = df.mean(axis=1)
top = df.sort_values(by='mean', ascending=False).iloc[:box_num, :]
top.reset_index(inplace=True)
values = [i for i in top.columns if 'impt' in i]
melted = pd.melt(top, id_vars=['features'], value_vars=values)
fig, ax = plt.subplots(figsize=(40, 30))
ax = sns.boxplot(x='features', y='value', data=melted)
new_labels = [item.get_text().title() for item in ax.get_xticklabels()]
ax.set_xticklabels(new_labels, rotation=90)
ax.set_xlabel("Features",fontsize=20)
ax.set_ylabel("Importance",fontsize=20)
ax.tick_params(labelsize=15, length=6, width=2)

# This is for use with feat_impt.txt, to see positions of random numbers
# after sorting by mean
# sort_mean = df.sort_values(by='mean', ascending=False)
# sort_mean.index.get_loc('random_1')
# Out[58]: 129

# sort_mean.index.get_loc('random_2')
# Out[59]: 75

# sort_mean.index.get_loc('random_3')
# Out[60]: 121

