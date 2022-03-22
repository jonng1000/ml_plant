# -*- coding: utf-8 -*-
"""
Created on Tue Feb 9 15:25:01 2021

@author: weixiong001

Plots feature importances on some dge and GO terms tested with my rf workflow
"""
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './dge_results/'

# Gets list of feature importance files
all_files = [a_file for a_file in os.listdir(DATA_FOLDER)]
fi_list = [one for one in all_files if one.endswith('_fi.txt')]

# Create dataframe from random forest's feature importance
df_lst = []
for one in fi_list:
    file_path = DATA_FOLDER + '/' + one
    # Reads in dataset, takes ~1 min
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    cols = data.columns[data.columns.str.startswith('rf')]
    data = data.loc[:, cols]
    class_label = one.split('_fi')[0]
    data.index.name = class_label + '_features'
    df_lst.append(data)

# Plotting
for one_df in df_lst:
    #one_loc_fi = df.loc[:, one_loc].copy()
    one_df.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
    one_df['mean'] = one_df.mean(axis=1)
    sorted_fi = one_df.sort_values(['mean'], ascending=False)
    top = sorted_fi.iloc[:20, :]
    top.reset_index()
    top = top.reset_index()
    melted = pd.melt(top, id_vars=[top.columns[0]], 
                     value_vars=['run_1', 'run_2', 'run_3', 'run_4', 'run_5'])
    
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(7, 7))
    # Feature names are on x-axis, feature values are on y-axis 
    sns.lineplot(data=melted, x=top.columns[0], y='value', ci=None, marker= 'o', sort=False)
    sns.stripplot(data=melted, x=top.columns[0], y='value', color='r')
    ax.xaxis.set_tick_params(rotation=90, labelsize=12)
    ax.set_xlabel('Features', fontsize=12)
    ax.set_ylabel('Feature importance', fontsize=12)
    plt.tight_layout()
    plt.savefig(top.columns[0] + '.png')
    plt.close()

