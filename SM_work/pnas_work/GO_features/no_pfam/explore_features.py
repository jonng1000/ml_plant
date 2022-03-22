# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

INPUT = 'feat'
BOX_NUM = 50

dataf_list = []
for file in os.listdir():
    if file.endswith('_' + INPUT + '.txt'):
        dataf = pd.read_csv(file, sep="\t", index_col=0)
        go_term = file.split('_' + INPUT)[0]
        dataf['GO term'] = go_term
        dataf['mean'] = dataf.mean(axis=1)
        top = dataf.sort_values(by='mean', ascending=False).iloc[:BOX_NUM, :]
        top.reset_index(inplace=True)
        values = [i for i in top.columns if 'impt' in i]
        melted = pd.melt(top, id_vars=['features'], value_vars=values)
        fig, ax = plt.subplots(figsize=(20, 15))
        ax = sns.boxplot(x='features', y='value', data=melted)
        new_labels = [item.get_text().title() for item in ax.get_xticklabels()]
        ax.set_xticklabels(new_labels, rotation=90)
        ax.set_xlabel("Features",fontsize=20)
        ax.set_ylabel("Importance",fontsize=20)
        ax.tick_params(labelsize=15, length=6, width=2)
        plt.tight_layout()
        plt.savefig(go_term + '_feat.png')
        # Preparing dataframes to create a lineplot downstream
        short = dataf.sort_values(by='mean', ascending=False) \
            .loc[:,['GO term', 'mean']].copy()
        short['n_f'] = range(1, len(short.index)+1)
        dataf_list.append(short)
plt.clf()

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

n_f1000 = all_df.loc[all_df['n_f'] <= 1000, :]
fig, ax = plt.subplots()
ax = sns.relplot(x="n_f", y="mean", col="GO term", data=n_f1000,
                 kind="line", col_wrap=4)
# plural since this goes to FacetGrid
# singular if using matplotlib
ax.set_xlabels("number of features")
plt.tight_layout()
plt.savefig('feat1000_i.png')
plt.clf()
