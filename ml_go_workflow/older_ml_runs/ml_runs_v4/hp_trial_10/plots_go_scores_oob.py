# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it. For go terms.
Plots oob score
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'


def get_scores_lst(folder):
    """
    Get all files in a folder, and from this, select only scores file,
    and returns it as a list of files
    """
    all_files = [a_file for a_file in os.listdir(folder)]
    scores_list = [one for one in all_files if one.endswith('_scores.txt')]
    return scores_list


def produce_df_lst(scores_list, folder):
    """
    From list of scores files, read in all their dataframes to form a list of
    them
    """
    df_lst = []
    for one in sl_orig:
        file_path = DATA_FOLDER + '/' + one
        go_term = one.split('_')[1] + '_' + one.split('_')[2]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=go_term)
        df_lst.append(data)
    return df_lst
 

# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
# List of scores as df
lst_df = produce_df_lst(sl_orig, DATA_FOLDER)
df_orig = pd.concat(lst_df, axis=0)
# Insert random colum into each df
df_orig.insert(loc=1, column='random', value='n')

# Did this hack so that the rest of the script can run
combined_df = df_orig

# Sorts by class_label, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('class_label')

# This section is for plotting
# Get names of scores e.g. f1
score_names = combined_df.columns[~combined_df.columns.
                                  isin(['class_label', 'model_name', 'random'])]
# Long form for seaborn
melted = pd.melt(combined_df, id_vars=['class_label', 'model_name', 'random'],
                 value_vars=score_names)
# f1, precision, recall
melted_oob = melted.loc[melted['variable'].isin(['oob_score'])]

score_types = ['oob_score']
for each in score_types:
    # Plotting
    if each == 'oob_score':
        data_used = melted_oob
        save = 'scores_oob.svg'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=data_used, x='class_label', y='value', hue='model_name',
                 style='random', ci=None, marker= 'o', sort=False)
    ax.xaxis.set_tick_params(rotation=90, labelsize=12)
    ax.set_xlabel('Class_label', fontsize=12)
    ax.set_ylabel('oob_score', fontsize=12)
    ax.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(save)
    plt.close()
