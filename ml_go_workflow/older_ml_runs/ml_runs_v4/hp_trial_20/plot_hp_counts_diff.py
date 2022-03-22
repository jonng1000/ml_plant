# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:33:36 2021

@author: weixiong001

Plots hp tests results
Different from plot_hp_counts.py as this counts each set of parameters as one
group, instead of splitting up and counting each parameter individually
"""


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from textwrap import wrap

FILE = './all_hp_counts_diff.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

for score in ['high', 'med', 'low']:
    selected = data.loc[data['score'] == score, :]
    temp = selected.drop(columns=['score', 'count'])
    temp_score = selected.loc[:, 'score']
    temp_count = selected.loc[:, 'count']
    added = temp.astype(str).apply(lambda x : x.name + '_' + x)
    added_again = added.apply('_'.join, axis=1)
    added_again.name = 'param_set'
    
    df_plot = pd.concat([temp_score, added_again, temp_count], axis=1)
    df_plot['param_set'] = ['\n'.join(wrap(x, 60)) for x in  df_plot['param_set']]
    picture = score + '_diff.svg'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=df_plot, x='param_set', y='count', 
                 ci=None, marker= 'o', sort=False)
    ax.xaxis.set_tick_params(rotation=90, labelsize=7)
    plt.margins(x=0.01)
    plt.tight_layout()
    plt.savefig(picture)
    plt.close()