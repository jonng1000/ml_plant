# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

dataf_list = []
for file in os.listdir():
    if file.endswith('_scores.txt'):
        dataf = pd.read_csv(file, sep="\t", index_col=0)
        go_term = file.split('_scores')[0]
        dataf['GO term'] = go_term
        melted = pd.melt(dataf, id_vars=['GO term'],
                         value_vars=['f1', 'precision', 'recall'])
        melted.rename(columns={'variable': 'metric'}, inplace=True)
        dataf_list.append(melted)

all_df = pd.concat(dataf_list).reset_index(drop=True)
fig, ax = plt.subplots()
# sns.catplot() returns a FacetGrid object for drawing subplots
ax = sns.catplot(x="metric", y="value", col="GO term", data=all_df,
                 kind="box", col_wrap=4)
# Gets ytick labls, axes is the container for the individual axes obj
#x.axes[0].get_yticklabels()
plt.savefig('all_scores.png')
plt.clf()