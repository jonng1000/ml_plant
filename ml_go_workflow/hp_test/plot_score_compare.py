# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it. For go terms.
Compares default and optimised hps.
Plots oob score
Modified from plots_go_scores_oob.py from 
D:/GoogleDrive/machine_learning/ml_go_workflow/ml_runs_v4/hp_trial_10
Includes both f1 and accuracy score
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './all_results/output_71ohp/'
DATA_FOLDER2 = './all_resu/results_dhp/'

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
    for one in scores_list:
        file_path = folder + '/' + one
        go_term = one.split('_')[1] + '_' + one.split('_')[2]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=go_term)
        df_lst.append(data)
    return df_lst
 
    
def combine(the_folder):
    """
    Combine all the score dataframes from one expt, to form one dataframe
    containing all the scores
    """
    # List of scores files
    sl_orig = get_scores_lst(the_folder)
    # List of scores as df
    lst_df = produce_df_lst(sl_orig, the_folder)
    df_orig = pd.concat(lst_df, axis=0)
    return df_orig


opt_hp = combine(DATA_FOLDER)
d_hp = combine(DATA_FOLDER2)
# Insert column showing if hp optimisation was carried out
opt_hp.insert(loc=1, column='optimise', value='y')
d_hp.insert(loc=1, column='optimise', value='n')

combined_df = pd.concat([opt_hp, d_hp], axis=0)
# Sorts by class_label, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('class_label')

# This section is for plotting
# Get names of scores e.g. f1
score_names = combined_df.columns[~combined_df.columns.
                                  isin(['class_label', 'model_name',
                                        'optimise'])
                                  ]
# Long form for seaborn
melted = pd.melt(combined_df, id_vars=['class_label', 'model_name', 'optimise'],
                 value_vars=score_names)
# oob acc and f1
melted_acc = melted.loc[melted['variable'].isin(['oob_accuracy']), :].copy()
melted_f1 = melted.loc[melted['variable'].isin(['oob_f1']), :].copy()
# Some datasets do not have this value as float, so need to change it
melted_f1.loc[:, 'value'] = melted_f1['value'].astype('float')
melted_acc.loc[:, 'value'] = melted_acc['value'].astype('float')

melted_acc = melted_acc.sort_values(by=['optimise', 'value'], ascending=False)
melted_f1 = melted_f1.sort_values(by=['optimise', 'value'], ascending=False)

# Making line plots
score_types = ['oob_accuracy', 'oob_f1']
for each in score_types:
    # Plotting
    if each == 'oob_accuracy':
        data_used = melted_acc
        save = 'compare_hp_acc.png'
    if each == 'oob_f1':
        data_used = melted_f1
        save = 'compare_hp_f1.png'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=data_used, x='class_label', y='value', hue='optimise',
                 ci=None, linestyle='', marker='o', sort=False)
    ax.xaxis.set_tick_params(rotation=90, labelsize=12)
    ax.set_xlabel('Class_label', fontsize=12)
    ax.set_ylabel('oob_score', fontsize=12)
    # Did not set legend size here, as making it bigger cuts of legend title
    plt.tight_layout()
    plt.savefig(save)
    plt.close()

# Making boxplots
fig, ax = plt.subplots()
sns.boxplot(data=melted_acc, x='optimise', y='value')
ax.set_ylabel('oob_acc')
plt.savefig('boxplot_acc.png')
plt.close()

fig, ax = plt.subplots()
sns.boxplot(data=melted_f1, x='optimise', y='value')
ax.set_ylabel('oob_f1')
plt.savefig('boxplot_f1.png')
plt.close()

