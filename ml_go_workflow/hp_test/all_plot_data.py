# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces a dataset for plotting raincloud plot 
(another folder). Modified from plot_lineplot_compare_all_v2.py. This is info
on hp influence on scores/
"""

import os
import pandas as pd
from textwrap import wrap

# For 71 GO classes
DATA_FOLDER = './all_results/results_71_ohp/'
DATA_FOLDER2 = './all_results/output_71chp/'
DATA_FOLDER3 = './all_results/output_71g1hp/'
DATA_FOLDER4 = './all_results/output_71g2hp/'
DATA_FOLDER5 = './all_results/results_dhp/'

FILE = 'G:/My Drive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
OUTPUT = 'all_data_plotting.txt'


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


# GO file
go_df = pd.read_csv(FILE, sep='\t', index_col=0)

# Creating dataframes
opt_hp = combine(DATA_FOLDER)
opt_hp2 = combine(DATA_FOLDER2)
opt_hp3 = combine(DATA_FOLDER3)
opt_hp4 = combine(DATA_FOLDER4)
d_hp = combine(DATA_FOLDER5)
# Insert column showing if hp optimisation, chosen hps or
# default hps were used
opt_hp.insert(loc=1, column='hp_type', value='rs_optimised')
opt_hp2.insert(loc=1, column='hp_type', value='chosen')
opt_hp3.insert(loc=1, column='hp_type', value='chosen_g1')
opt_hp4.insert(loc=1, column='hp_type', value='chosen_g2')
d_hp.insert(loc=1, column='hp_type', value='default')

combined_df = pd.concat([opt_hp, opt_hp2, opt_hp3, opt_hp4, d_hp], axis=0)
# Sorts by class_label, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('class_label')


# This section is for plotting
# Get names of scores e.g. f1
score_names = combined_df.columns[~combined_df.columns.
                                  isin(['class_label', 'model_name',
                                        'hp_type'])
                                  ]
# Long form for seaborn
melted = pd.melt(combined_df, id_vars=['class_label', 'model_name', 'hp_type'],
                 value_vars=score_names)
# oob f1
melted_f1 = melted.loc[melted['variable'].isin(['oob_f1']), :].copy()
# Some datasets do not have this value as float, so need to change it
melted_f1.loc[:, 'value'] = melted_f1['value'].astype('float')
melted_f1 = melted_f1.sort_values(by=['hp_type', 'value'], ascending=False)


new_go_names =  melted_f1['class_label'].str.replace('_', ':', regex=False)
melted_f1['GO_desc'] = new_go_names
map_dict = go_df['GO_desc'].to_dict()
melted_f1 = melted_f1.replace({'GO_desc': map_dict})
melted_f1['edit_GO_desc'] = ['\n'.join(wrap(x, 20, break_long_words=False)) 
                             for x in  melted_f1['GO_desc']]

melted_f1.index.name = 'id'
melted_f1.to_csv(OUTPUT, sep='\t')
