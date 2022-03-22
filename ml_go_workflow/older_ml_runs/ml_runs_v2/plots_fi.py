# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:01 2020

@author: weixiong001

Plots feature importance
"""
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'


all_files = [a_file for a_file in os.listdir(DATA_FOLDER)]
fi_list = [one for one in all_files if one.endswith('_fi.txt')]

selected = []
for one_file in fi_list:
    if one_file.startswith('rf'):
        selected.append(one_file)

df_lst = []
for one in selected:
    file_path = DATA_FOLDER + '/' + one
    # model name
    model_name = one.split('_')[0]
    # Reads in dataset, takes ~1 min
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    # Insert is in place
    data.insert(loc=0, column='model_name', value=model_name)
    df_lst.append(data)

df = pd.concat(df_lst, axis=1)

plastid_fi = df.loc[:, 'plastid_importance'].copy()
plastid_fi.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
plastid_fi['mean'] = plastid_fi.mean(axis=1)
sorted_fi = plastid_fi.sort_values(['mean'], ascending=False)
top = sorted_fi.iloc[:20, :]
top.reset_index()
top = top.reset_index()
melted = pd.melt(top, id_vars=['index'], 
                 value_vars=['run_1', 'run_2', 'run_3', 'run_4', 'run_5'])

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 7))
sns.lineplot(data=melted, x='index', y='value', ci=None, marker= 'o', sort=False)
sns.stripplot(data=melted, x='index', y='value')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('plastid.png')

# plastid below is a place holder, rem to generalise in future
plastid_fi = df.loc[:, 'cytosol_importance'].copy()
plastid_fi.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
plastid_fi['mean'] = plastid_fi.mean(axis=1)
sorted_fi = plastid_fi.sort_values(['mean'], ascending=False)
top = sorted_fi.iloc[:20, :]
top.reset_index()
top = top.reset_index()
melted = pd.melt(top, id_vars=['index'], 
                 value_vars=['run_1', 'run_2', 'run_3', 'run_4', 'run_5'])

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 7))
sns.lineplot(data=melted, x='index', y='value', ci=None, marker= 'o', sort=False)
sns.stripplot(data=melted, x='index', y='value')
ax.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig('cytosol.png')
