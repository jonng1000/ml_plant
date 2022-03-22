# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'


all_files = [a_file for a_file in os.listdir(DATA_FOLDER)]

scores_list = [one for one in all_files if one.endswith('c16_scores.txt')]

df_lst = []
for one in scores_list:
    file_path = DATA_FOLDER + '/' + one
    # model name
    model_name = one.split('_')[0]
    # Reads in dataset, takes ~1 min
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    # Insert is in place
    data.insert(loc=0, column='model_name', value=model_name)
    df_lst.append(data)


df = pd.concat(df_lst, axis=0)

# Get names of scores e.g. f1
score_names = df.columns[~df.columns.isin(['cell_loc', 'model_name'])]
# Long form for seaborn
melted = pd.melt(df, id_vars=['cell_loc', 'model_name'], 
                 value_vars=score_names)
# Rename model names so that its easier to work with
map_dict = {md: md[:-1] for md in set(melted['model_name'])}
melted = melted.replace({'model_name': map_dict})
# f1, precision, recall
melted_3scores = melted.loc[melted['variable'].isin(['f1', 
                                                     'precision', 'recall'])]
melted_f1 = melted.loc[melted['variable'].isin(['f1'])]
melted_pre = melted.loc[melted['variable'].isin(['precision'])]
melted_rec = melted.loc[melted['variable'].isin(['recall'])]

score_types = ['f1', 'precision', 'recall']
for each in score_types:
    # Plotting
    if each == 'f1':
        data_used = melted_f1
        save = 'scores_f1.png'
    elif each == 'precision':
        data_used = melted_pre
        save = 'scores_pre.png'
    elif each == 'recall':
        data_used = melted_rec
        save = 'scores_rec.png'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))

    sns.lineplot(data=data_used, x='cell_loc', y='value', hue='model_name',
                 style='variable', ci=None, marker= 'o', sort=False)
    sns.stripplot(data=data_used, x='cell_loc', y='value', 
                hue='model_name')
    ax.xaxis.set_tick_params(rotation=90)
    handles, labels = ax.get_legend_handles_labels()
    l = plt.legend(handles[0:8], labels[0:8])
    plt.tight_layout()
    plt.savefig(save)
    #plt.clf()
    plt.close()

# seaborn doesnt seem to do this correctly, use the below
# https://stackoverflow.com/questions/37619952/drawing-points-with-with-median-lines-in-seaborn-using-stripplot
