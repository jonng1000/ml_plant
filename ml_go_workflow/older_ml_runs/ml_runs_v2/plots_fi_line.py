# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:01 2020

@author: weixiong001

Plots feature importances for all 16 cellular locations, based on
plots_fi_v2.py. Draws a line corresponding to the feature importances
from randomised feature values

Used to see how its like, but it is not used
"""
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'
RAN_FI = './top20_fi_ran.txt'

top20_ran = pd.read_csv(RAN_FI, sep='\t', index_col=0)
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
# Plotting
for one_loc in cell_loc:
    one_loc_fi = df.loc[:, one_loc].copy()
    one_loc_fi.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
    one_loc_fi['mean'] = one_loc_fi.mean(axis=1)
    sorted_fi = one_loc_fi.sort_values(['mean'], ascending=False)
    top = sorted_fi.iloc[:20, :]
    top.reset_index()
    top = top.reset_index()
    melted = pd.melt(top, id_vars=['index'], 
                     value_vars=['run_1', 'run_2', 'run_3', 'run_4', 'run_5'])
    ran_fi = top20_ran[one_loc.split('_importance')[0]]

    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=melted, x='index', y='value', ci=None, marker= 'o', sort=False)
    sns.stripplot(data=melted, x='index', y='value')
    ax.xaxis.set_tick_params(rotation=90)
    sns.lineplot(data=ran_fi, color='red', ci=None, marker= 'o', sort=False)
    plt.tight_layout()
    loc_name = one_loc.split('_importance')[0]
    plt.savefig(loc_name + '.png')
    plt.close()

