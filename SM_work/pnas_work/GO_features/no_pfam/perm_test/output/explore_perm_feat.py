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
        
        selected_itr = dataf.loc[dataf.loc[:, 'itr'] == SEl_ITR, :]
        only_data2 = selected_itr.drop(columns=['perm', 'itr'])
        top2 = only_data2.mean().sort_values(ascending=False)[:NUM]
        sel_lst2 = ['perm', 'itr'] + list(top2.index)
        selection2 = selected_itr.loc[:, sel_lst2]
        melted2 = pd.melt(selection2, value_vars=top2.index)
        #fig, ax = plt.subplots(figsize=(20, 15))
        ax = sns.boxplot(x='variable', y='value', data=melted2)
        new_labels = [item.get_text().title() for item in ax.get_xticklabels()]
        ax.set_xticklabels(new_labels, rotation=90)
        ax.set_xlabel("Features",fontsize=20)
        ax.set_ylabel("Importance",fontsize=20)
        ax.tick_params(labelsize=15, length=6, width=2)
        plt.tight_layout()
        plt.savefig(key_name + '_ itr_' + str(SEl_ITR) + '_feat.png')
        plt.clf()
        
        only_data3 = selection.drop(columns=['perm'])
        melted3 = pd.melt(only_data3.groupby('itr').mean(), value_vars=top.index)
        #fig, ax = plt.subplots(figsize=(20, 15))
        ax = sns.boxplot(x='variable', y='value', data=melted3)
        new_labels = [item.get_text().title() for item in ax.get_xticklabels()]
        ax.set_xticklabels(new_labels, rotation=90)
        ax.set_xlabel("Features",fontsize=20)
        ax.set_ylabel("Importance",fontsize=20)
        ax.tick_params(labelsize=15, length=6, width=2)
        plt.tight_layout()
        plt.savefig(key_name + '_ all_itr_feat.png')
        plt.clf()