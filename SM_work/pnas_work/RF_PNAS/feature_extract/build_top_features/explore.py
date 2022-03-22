# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:22:03 2020

@author: weixiong001

Plots scores from build_RF_score_ran.py and build_RF_score.py
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

non_random = 'rfm_scores.txt'
random = 'rfm_scores_ran.txt'

df_nr = pd.read_csv(non_random, sep="\t", index_col=0)
df_r = pd.read_csv(random, sep="\t", index_col=0)
all_df = pd.concat([df_nr, df_r])
all_df.reset_index(drop=True, inplace=True)

mean_scores = all_df.groupby(['random', 'num_features']).mean().reset_index()
melted = pd.melt(mean_scores, id_vars=['random', 'num_features'],
                 value_vars=['f1', 'precision', 'recall'])
melted.rename(columns={'variable': 'metric'}, inplace=True)

fig, ax = plt.subplots()
ax = sns.lineplot(x="num_features", y="value",
                  hue="random", style="metric", markers=True, data=melted)
ax.set_xticks([i for i in range(10, 101, 10)])
ax.set_yticks([i/10 for i in range(5, 10)])
ax.set_ylabel("score")
plt.savefig('scores_building.png')