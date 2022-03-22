# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:54:09 2019

@author: weixiong001

Ensemble model by varying alpha (threshold to convert average labels 
[in fractions] into 0s and 1s for individual models)
"""

import pandas as pd
import math
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("combined_scores.csv", sep="\t", index_col=0)
df.drop(columns='index', inplace=True)
df['Precision'] = df['tp'] / (df['tp'] + df['fp'])
df['Recall'] = df['tp'] / (df['tp'] + df['fn'])
df['F1'] = 2 * df['Precision'] * df['Recall'] / (df['Precision'] + 
                                                  df['Recall'])
melted = pd.melt(df, id_vars=['ml'], 
                 value_vars=['Precision','Recall', 'F1']
                 )
melted.rename(columns={"dtc": "DTC", "knn": "KNN", "mlp": "MLP", "rf": "RF",
                       "svm": "SVM"}, inplace=True )
fig1, ax1 = plt.subplots(figsize=(20, 15))
sns.set_context(font_scale=3)
ax = sns.boxplot(x="ml", y="value", hue="variable", data=melted, ax=ax1)
new_labels = [item.get_text().upper() for item in ax.get_xticklabels()]
ax.set_xticklabels(new_labels)
ax.set_xlabel("Model",fontsize=20)
ax.set_ylabel("Scores",fontsize=20)
# labelsize changes size of labels
# length and width changes size of ticks
ax.tick_params(labelsize=20, length=6, width=2)
ax.legend(markerscale=4, fontsize=16)
# Need to shift position of legend, so need to save in pdf instead of png
# Change to png just to show Marek
plt.savefig("model_scores.png")

