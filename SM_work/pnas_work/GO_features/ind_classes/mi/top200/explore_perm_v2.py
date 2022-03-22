# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001

Shows top NUM features (NUM is a constant which is defined below),
defined by permutation importance. Edited from explore_perm_feat.py
in D:\GoogleDrive\machine_learning
\GO_features\no_pfam\perm_test\output
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

NUM = 50

fig, ax = plt.subplots(figsize=(20, 15))
for file in os.listdir():
    if file.endswith('_perm.txt'):
        key_name = file.split('_perm.txt')[0]
        dataf = pd.read_csv(file, sep="\t", index_col=0)
        only_data = dataf.drop(columns=['perm', 'itr'])
        top = only_data.mean().sort_values(ascending=False)[:NUM]
        sel_lst = ['perm', 'itr'] + list(top.index)
        selection = dataf.loc[:, sel_lst]
        melted = pd.melt(selection, value_vars=top.index)

        ax = sns.boxplot(x='variable', y='value', data=melted)
        new_labels = [item.get_text().title() for item in ax.get_xticklabels()]
        ax.set_xticklabels(new_labels, rotation=90)
        ax.set_xlabel("Features",fontsize=20)
        ax.set_ylabel("Importance",fontsize=20)
        ax.tick_params(labelsize=15, length=6, width=2)
        plt.tight_layout()
        plt.savefig(key_name + '_feat.png')
        plt.clf()
        