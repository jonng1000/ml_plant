# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it. For 16 cell
locations, modified from plots_cell_loc_scores.py in
D:\GoogleDrive\machine_learning\ml_go_workflow\time_trial

Also plots time taken. No error bar.
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
        class_label = one.split('_scores')[0]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=class_label)
        df_lst.append(data)
    return df_lst
 

# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
# List of scores as df
lst_df = produce_df_lst(sl_orig, DATA_FOLDER)
df_orig = pd.concat(lst_df, axis=0)

df_orig['time_start'] = pd.to_datetime(df_orig['time_start'], dayfirst=True)
df_orig['time_end'] = pd.to_datetime(df_orig['time_end'], dayfirst=True)
df_orig['time_taken'] = df_orig['time_end'] - df_orig['time_start']
df_orig['time_taken_(s)'] = df_orig['time_taken'].astype('timedelta64[s]')

selected = df_orig[['class_label', 'model_name', 'time_taken_(s)']]
model_mean = selected.groupby('model_name').mean().reset_index()
model_mean['time_taken_(min)'] = model_mean['time_taken_(s)']/60
model_mean['cores'] = model_mean['model_name'].str[2:]
model_mean['cores'] = model_mean['cores'].astype('int64')
model_mean.sort_values(by=['cores'], inplace=True)

# To prevent seaborn from treating this as integer
model_mean['cores'] = model_mean['cores'].astype('str')
save = 'cores_time.png'
fig, ax = plt.subplots()
#fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(data=model_mean, x='cores', y='time_taken_(min)',
             ci=None, marker= 'o', sort=False)
#ax.set(xticks=model_mean['cores'].values)
#ax.set_xticks(range(len(model_mean)))
#ax.set_xticklabels(model_mean['cores'])
ax.set_xlabel('Cores', fontsize=12)
ax.set_ylabel('time_taken_(s)', fontsize=12)
plt.tight_layout()
plt.savefig(save)
plt.close()
