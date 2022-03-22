# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it.
Uses both original and randomised feature values, for its plot,
to show its difference

Based on plots_c16.py
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'
DATA_FOLDER_RAN = './results_ran/'


def get_scores_lst(folder):
    """
    Get all files in a folder, and from this, select only scores file,
    and returns it as a list of files
    """
    all_files = [a_file for a_file in os.listdir(folder)]
    scores_list = [one for one in all_files if one.endswith('c16_scores.txt')]
    return scores_list


def produce_df(scores_list, folder):
    """
    From list of scores files, read in all their dataframes, and concat to
    form one dataframe
    """
    df_lst = []
    for one in scores_list:
        file_path = folder + '/' + one
        # model name
        model_name = one.split('_')[0]
        # Reads in dataset, takes ~1 min
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        # Insert is in place
        data.insert(loc=0, column='model_name', value=model_name)
        df_lst.append(data)
    df = pd.concat(df_lst, axis=0)
    return df


def replace_model_name(df):
    """
    Rename model names so that its easier to work with
    """
    # mapping dict for renaming
    map_dict = {md: md[:-1] for md in set(df['model_name'])}
    df = df.replace({'model_name': map_dict})
    return df


# These two variables has the list of scores files for original dataset, and
# the dataset with random feature values
sl_orig = get_scores_lst(DATA_FOLDER)
sl_ran = get_scores_lst(DATA_FOLDER_RAN)

# These two variables has the list of scores files for original dataset, and
# the dataset with random feature values
df_orig = produce_df(sl_orig, DATA_FOLDER)
df_ran = produce_df(sl_ran, DATA_FOLDER_RAN)
# Replace model names in df
df_orig = replace_model_name(df_orig)
df_ran = replace_model_name(df_ran)

# mapping to rename cell locations in random dataset
mapping = {md: md.split('_ran')[0] for md in set(df_ran['cell_loc'])}
df_ran = df_ran.replace({'cell_loc': mapping})
# Insert random colum into each df
df_ran.insert(loc=1, column='random', value='y')
df_orig.insert(loc=1, column='random', value='n')
# Combines both df
combined_df = pd.concat([df_orig, df_ran])
# Sorts by cell location, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('cell_loc')

# This section is for plotting
# Get names of scores e.g. f1
score_names = combined_df.columns[~combined_df.columns.
                                  isin(['cell_loc', 'model_name', 'random'])]
# Long form for seaborn
melted = pd.melt(combined_df, id_vars=['cell_loc', 'model_name', 'random'],
                 value_vars=score_names)
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
        save = 'scores_f1.svg'
    elif each == 'precision':
        data_used = melted_pre
        save = 'scores_pre.svg'
    elif each == 'recall':
        data_used = melted_rec
        save = 'scores_rec.svg'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=data_used, x='cell_loc', y='value', hue='model_name',
                 style='random', ci=None, sort=False)
    sns.stripplot(data=data_used, x='cell_loc', y='value',
                  hue='model_name')
    ax.xaxis.set_tick_params(rotation=90, labelsize=12)
    ax.set_xlabel('Cell location', fontsize=12)
    ax.set_ylabel('F1', fontsize=12)
    ax.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(save)
    plt.close()
