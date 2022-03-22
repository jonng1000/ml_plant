# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Combines scores from GO features obtained from various methods.
"""

import os
import numpy as np
import pandas as pd

DATA_FOLDER = './output_interpro/'
DATA_FOLDER2 = './output_tair/'
DATA_FOLDER3 = 'D:/GoogleDrive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4/'
OUTPUT = 'combined_scores.txt'

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
        file_path = folder + '/' + one
        go_term = one.split('_')[1] + '_' + one.split('_')[2]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=go_term)
        df_lst.append(data)
    return df_lst
 

# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
sl_orig2 = get_scores_lst(DATA_FOLDER2)
sl_orig3 = get_scores_lst(DATA_FOLDER3)
# List of scores as df
lst_df = produce_df_lst(sl_orig, DATA_FOLDER)
lst_df2 = produce_df_lst(sl_orig2, DATA_FOLDER2)
lst_df3 = produce_df_lst(sl_orig3, DATA_FOLDER3)
# Makes df with scores
df_orig = pd.concat(lst_df, axis=0)
df_orig = df_orig.set_index('class_label')
df_orig.insert(0, 'feature_type', 'interpro_GO')
df_orig2 = pd.concat(lst_df2, axis=0)
df_orig2 = df_orig2.set_index('class_label')
df_orig2.insert(0, 'feature_type', 'tair_GO_comp')
df_orig3 = pd.concat(lst_df3, axis=0)
df_orig3 = df_orig3.set_index('class_label')
df_orig3.insert(0, 'feature_type', 'all_features')

combined_df = pd.concat([df_orig, df_orig2, df_orig3], axis=0)
combined_df = combined_df.reset_index()
combined_df.index.name = 'id'

combined_df.to_csv(OUTPUT, sep='\t')
