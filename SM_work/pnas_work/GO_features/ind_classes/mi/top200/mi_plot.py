# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001

Shows top NUM features (NUM is a constant which is defined below),
defined by mutual information (mi).
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

NUM = 50
FILE = 'mi_golgi.txt'
IMAGE = 'mi_golgi.png'

dataf = pd.read_csv(FILE, sep='\t', index_col=0).reset_index()
top = dataf[1:NUM+1]
fig, ax = plt.subplots(figsize=(20, 15))
# Need to put sort=False to prevent seaborn from sorting x-axis
# labels
ax = sns.lineplot(x=top['Features'], y=top['mi'], sort=False)
new_labels = top['Features']
ax.set_xticklabels(new_labels, rotation=90)
ax.set_xlabel('Features',fontsize=20)
ax.set_ylabel('MI',fontsize=20)
ax.tick_params(labelsize=15, length=6, width=2)
plt.tight_layout()
plt.savefig(IMAGE)
plt.clf()
