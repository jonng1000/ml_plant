# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:01 2020

@author: weixiong001

Plots feature importances for all 16 cellular locations, based on
plots_fi.py. For testing purpose, not used
"""
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'

# Gets list of feature importance files
all_files = [a_file for a_file in os.listdir(DATA_FOLDER)]
fi_list = [one for one in all_files if one.endswith('_fi.txt')]
# Selects only random forest feature importance files
selected = []
for one_file in fi_list:
    if one_file.startswith('rf'):
        selected.append(one_file)
# Create dataframe from random forest's feature importance
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
cell_loc = {name for name in df.columns if name.endswith('_importance')}

# Added here as a hack to select stuff
cl_select = ['plastid', 'plastid_stroma', 'cytosol', 'membrane']
cl_s_lst = []
for x in cell_loc:
    for y in cl_select:
        if y == x.split('_importance')[0]:
            cl_s_lst.append(x)

# Continuing the hack
new_df_lst = []
for one_loc in cl_s_lst:
    one_loc_fi = df.loc[:, one_loc].copy()
    one_loc_fi.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
    one_loc_fi['mean'] = one_loc_fi.mean(axis=1)
    sorted_fi = one_loc_fi.sort_values(['mean'], ascending=False)
    top = sorted_fi.iloc[:20, :]
    top.reset_index()
    top = top.reset_index()
    melted = pd.melt(top, id_vars=['index'], 
                     value_vars=['run_1', 'run_2', 'run_3', 'run_4', 'run_5'])
    melted['cell_loc'] = one_loc.split('_importance')[0]
    new_df_lst.append(melted)

new_df = pd.concat(new_df_lst, axis=0)

# Plotting
fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 7))

ax = sns.relplot(x='index', y='value', ci=None, marker= 'o', sort=False,
                 col='cell_loc', data=new_df, kind='line', col_wrap=2)
ax = sns.catplot(x='index', y='value', ci=None, marker= 'o',
                 col='cell_loc', data=new_df, kind='strip', col_wrap=2)

#sns.lineplot(data=melted, x='index', y='value', ci=None, marker= 'o', sort=False)
#sns.stripplot(data=melted, x='index', y='value', color='r')
ax.set_xlabels('Features', fontsize=12)
ax.set_ylabels('Feature importance', fontsize=12)

for ax1 in ax.axes:
    plt.setp(ax1.get_xticklabels(), visible=True, rotation=90)
plt.tight_layout()
# Continued hack here
plt.savefig('cell_loc_4.svg')
plt.close()

