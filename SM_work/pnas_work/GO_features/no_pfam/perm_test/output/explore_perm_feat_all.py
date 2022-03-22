# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

NUM = 50
SEl_ITR = 0

dataf_list = []

fig, ax = plt.subplots(figsize=(20, 15))
for file in os.listdir():
    if file.endswith('_perm.txt'):
        key_name = file.split('_perm.txt')[0]
        dataf = pd.read_csv(file, sep="\t", index_col=0)
        only_data = dataf.drop(columns=['perm', 'itr'])
        only_data_T = only_data.T
        only_data_T['mean'] = only_data_T.mean(axis=1)
        only_data_T['GO term'] = key_name
        # continue here
        short = only_data_T.sort_values(by='mean', ascending=False) \
            .loc[:,['GO term', 'mean']].copy()
        short['n_f'] = range(1, len(short.index)+1)
        dataf_list.append(short)

all_df = pd.concat(dataf_list).reset_index()
fig, ax = plt.subplots()
ax = sns.relplot(x="n_f", y="mean", col="GO term", data=all_df,
                 kind="line", col_wrap=4)
# plural since this goes to FacetGrid
# singular if using matplotlib
ax.set_xlabels("number of features")
plt.tight_layout()
plt.savefig('all_feat_i.png')
plt.clf()