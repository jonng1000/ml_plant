# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './scores_c16/'

df_lst = []
for a_file in os.listdir(DATA_FOLDER):
    file_path = DATA_FOLDER + '/' + a_file
    # cell location name
    model_name = a_file.split('_')[0]
    # Reads in dataset, takes ~1 min
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    # Insert is in place
    data.insert(loc=1, column='model_name', value=model_name)
    df_lst.append(data)

df = pd.concat(df_lst, axis=0)
# Get names of scores e.g. f1
score_names = df.columns[~df.columns.isin(['cell_loc', 'model_name'])]
# Long form for seaborn
melted = pd.melt(df, id_vars=['cell_loc', 'model_name'], 
                 value_vars=score_names)

# f1, precision, recall
melted_3scores = melted.loc[melted['variable'].isin(['f1', 
                                                     'precision', 'recall'])]
melted_f1 = melted.loc[melted['variable'].isin(['f1'])]
melted_pre = melted.loc[melted['variable'].isin(['precision'])]
melted_rec = melted.loc[melted['variable'].isin(['recall'])]

# Do this in a loop in futre
# Plotting
fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=melted_3scores, x='cell_loc', y='value', 
             hue='model_name', style='variable', ci=None, marker='o')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('scores_3.png')
plt.clf()

# Plotting
fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=melted_f1, x='cell_loc', y='value', 
             hue='model_name', style='variable', ci=None, marker='o')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('scores_f1.png')
plt.clf()

# Plotting
fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=melted_pre, x='cell_loc', y='value', 
             hue='model_name', style='variable', ci=None, marker='o')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('scores_pre.png')
plt.clf()

# Plotting
fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=melted_rec, x='cell_loc', y='value', 
             hue='model_name', style='variable', ci=None, marker='o')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('scores_rec.png')
plt.clf()