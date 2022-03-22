# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:56 2020

@author: weixiong001
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

INPUT = 'build_s'
BOX_NUM = 50

dataf_list = []
for file in os.listdir():
    if file.endswith('_' + INPUT + '.txt'):
        dataf = pd.read_csv(file, sep="\t", index_col=0)
        go_term = file.split('_' + INPUT)[0]
        dataf['GO term'] = go_term
        dataf_list.append(dataf)
all_df = pd.concat(dataf_list).reset_index(drop=True)
mean_scores = all_df.groupby(['GO term', 'random', 'num_features']) \
    .mean().reset_index()
melted = pd.melt(mean_scores, id_vars=['GO term', 'random', 'num_features'],
                 value_vars=['f1', 'precision', 'recall'])
melted.rename(columns={'variable': 'metric'}, inplace=True)

fig, ax = plt.subplots()
ax = sns.relplot(x="num_features", y="value", hue="random", style="metric",
                 col="GO term", data=melted, kind="line", col_wrap=4)
# # plural since this goes to FacetGrid
# # singular if using matplotlib
ax.set_xlabels("number of features")
ax.set_ylabels("score")
plt.savefig('all_build_s.png')
plt.clf()

melted1000 = melted.loc[melted['num_features'] <= 1000, :]
fig, ax = plt.subplots()
ax = sns.relplot(x="num_features", y="value", hue="random", style="metric",
                 col="GO term", data=melted1000, kind="line", col_wrap=4)
# # plural since this goes to FacetGrid
# # singular if using matplotlib
ax.set_xlabels("number of features")
ax.set_ylabels("score")
plt.savefig('build_s1000.png')
plt.clf()
