# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise it. For go terms.
Plots oob score
Modified from plots_go_scores_oobf1.py from 
D:\GoogleDrive\machine_learning\ml_go_workflow\hp_test
Includes both f1 and accuracy score
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './output4/'
GO_COUNTS = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
FIG = 'scatterplot_line.png'
FIG1 = 'scatterplot.png'

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
# Makes df with scores
df_orig = pd.concat(lst_df, axis=0)
df_orig = df_orig.set_index('class_label')
# Makes df with GO counts
go_counts = pd.read_csv(GO_COUNTS, sep='\t', index_col=0)
go_counts.index = go_counts.index.str.replace(':','_')
selection = go_counts.loc[:, 'Counts']
# Makes combined df
combined_df = pd.concat([df_orig, selection], join='inner', axis=1)
'''
# Ensures that no nan is present
combined_df.isna().any().any()
Out[79]: False
'''
# This section is for plotting
# To ensure my plotting code can run
data_used = combined_df

fig, ax = plt.subplots()
ax.set(xscale='log')
sns.regplot(data=data_used, x='Counts', y='oob_f1', logx=True)
sns.scatterplot(data=data_used, x='Counts', y='oob_f1')
plt.savefig(FIG)
plt.close()

fig, ax = plt.subplots()
sns.scatterplot(data=data_used, x='Counts', y='oob_f1')
plt.savefig(FIG1)
plt.close()