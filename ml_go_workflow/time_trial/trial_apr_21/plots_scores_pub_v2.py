# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it. For 16 cell
locations, modified from plots_scores_pub.py in
D:\GoogleDrive\machine_learning\ml_go_workflow\time_trial\trial_apr_21

Makes publication ready graphs, also produces a mapping table to make it easier
to map GO terms to their descriptions
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './results/'
FILE = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
OUTPUT = 'GO_term_desc.txt'

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
        class_label = one.split('_scores')[0]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=class_label)
        df_lst.append(data)
    return df_lst
 

# GO file
go_df = pd.read_csv(FILE, sep='\t', index_col=0)

# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
# List of scores as df
lst_df = produce_df_lst(sl_orig, DATA_FOLDER)
df_orig = pd.concat(lst_df, axis=0)
# Insert random colum into each df
df_orig.insert(loc=1, column='random', value='n')
# Did this hack so that the rest of the script can run
combined_df = df_orig

# Sorts by f1 value, just a rough sort
combined_df = combined_df.sort_values('f1')

# This section is for plotting
# Get names of scores e.g. f1
score_names = combined_df.columns[~combined_df.columns.
                                  isin(['class_label', 'model_name', 'random'])]
# Long form for seaborn
melted = pd.melt(combined_df, id_vars=['class_label', 'model_name', 'random'],
                 value_vars=score_names)
# f1, precision, recall
melted_3scores = melted.loc[melted['variable'].isin(['f1',
                                                     'precision', 'recall'])]
melted_f1 = melted.loc[melted['variable'].isin(['f1'])]
# Prevents the setting with copy warning
melted_f1 = melted_f1.copy()

go_names_temp = melted_f1['class_label'].str.split('go_').str[1]
new_go_names = go_names_temp.str.replace('_', ':', regex=False)
melted_f1['GO_desc'] = new_go_names
map_dict = go_df['GO_desc'].to_dict()
melted_f1 = melted_f1.replace({'GO_desc': map_dict})

score_types = ['f1', 'precision', 'recall']  # Outdated, but left it in for convenience
for each in score_types:
    # Plotting
    if each == 'f1':
        data_used = melted_f1
        save = 'scores_pub_f1_v2.svg'
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(data=data_used, x='GO_desc', y='value', hue='model_name')
    ax.xaxis.set_tick_params(rotation=90, labelsize=12)
    ax.set_xlabel('Class_label', fontsize=12)
    ax.set_ylabel('F1', fontsize=12)
    ax.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(save)
    plt.close()

table = melted_f1.loc[:, ['class_label', 'GO_desc']].drop_duplicates()
table.index.name = 'id'
table.to_csv(OUTPUT, sep='\t')

'''
melted_f1.groupby('model_name').mean()
Out[10]: 
               value
model_name          
ada         0.412886
brf         0.257836
logr        0.317169
lsv         0.350148
rf          0.427061
'''