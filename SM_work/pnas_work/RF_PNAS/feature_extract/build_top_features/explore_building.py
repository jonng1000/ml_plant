# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:22:03 2020

@author: weixiong001

Plots scores from build_RF_score_v2.py
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

scores100 = 'rfm_scores_100.txt'
scores1000 = 'rfm_scores_1000.txt'
scores9000 = 'rfm_scores_9000.txt'
scores9537 = 'rfm_scores_9537.txt'

upper_limit = 200

list_df = [pd.read_csv(i, sep="\t", index_col=0) for i in [scores100,
                                                           scores1000,
                                                           scores9000,
                                                           scores9537]
           ]
all_df = pd.concat(list_df).reset_index(drop=True)
# 100 features and 1000 features has been duplicated, ie ran twice due to
# bug in previous script used to generate scores, hence they need to be
# removed
# Removes duplicates from 100 features
# Below code identifies index to be removed
# all_df[all_df['num_features'] == 100]
all_df.drop(all_df.iloc[2000:2200, :].index, inplace=True)
all_df = all_df.reset_index(drop=True)
# Removes duplicates from 1000 features
# Below code identifies index to be removed
# all_df[all_df['num_features'] == 1000]
all_df.drop(all_df.iloc[3800:4000, :].index, inplace=True)
all_df = all_df.reset_index(drop=True)

mean_scores = all_df.groupby(['random', 'num_features']).mean().reset_index()
melted = pd.melt(mean_scores, id_vars=['random', 'num_features'],
                 value_vars=['f1', 'precision', 'recall'])
melted.rename(columns={'variable': 'metric'}, inplace=True)

fig, ax = plt.subplots(figsize=(6, 4))
ax = sns.lineplot(x="num_features", y="value",
                  hue="random", style="metric", data=melted)
new_x_ticks = [0] + [i for i in range(1000, 9001, 1000)] + [9537]
ax.set_xticks(new_x_ticks)
ax.set_xticklabels(new_x_ticks, rotation=45, ha='center')
ax.set_ylabel("score")
ax.set_xlabel("number of features")
plt.tight_layout()
plt.savefig('scores_build_all.png')
plt.clf()

mean_scores = mean_scores[mean_scores['num_features'] <= upper_limit]
melted = pd.melt(mean_scores, id_vars=['random', 'num_features'],
                  value_vars=['f1', 'precision', 'recall'])
melted.rename(columns={'variable': 'metric'}, inplace=True)
ax = sns.lineplot(x="num_features", y="value",
                  hue="random", style="metric", data=melted)
ax.set_ylabel("score")
ax.set_xlabel("number of features")
