# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:33:36 2021

@author: weixiong001

Plots hp tests results
"""


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = './all_hp_counts.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

for score in ['high', 'med', 'low']:
    selected = data.loc[data['score'] == score, :]
    
    picture = score + '.svg'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=selected, x='params', y='count', 
                 ci=None, marker= 'o', sort=False)
    ax.xaxis.set_tick_params(rotation=90)
    plt.tight_layout()
    plt.savefig(picture)
    plt.close()
    