# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:29:25 2021

@author: weixiong001

Compiles all categorical features scores, includes 54 tti_cluster ids as they
are categorical features and were as mislabelled as ttr_cluster ids 
(continuous features)
"""
import pandas as pd
import os
import csv


DATA_FOLDER = 'D:/GoogleDrive/machine_learning/ml_go_workflow/rest_catf_runs/output/'
TTI_FOLDER = 'D:/GoogleDrive/machine_learning/ml_go_workflow/tti_runs/output/'
OUTPUT = 'edited_catf_scores.txt'

def get_scores_lst(folder):
    """
    Get all files in a folder, and from this, select only scores file,
    and returns it as a list of files
    """
    all_files = [a_file for a_file in os.listdir(folder)]
    scores_list = [one for one in all_files if one.endswith('_scores.txt')]
    return scores_list


def produce_df_lst_v2(scores_list, folder):
    """
    From list of scores files, read in all their dataframes to form a list of
    them
    Modifed from the original function, to make it more general, so that it
    can be used on non GO term class labels
    """
    df_lst = []
    for one in scores_list:
        file_path = folder + '/' + one
        term = one.split('_scores')[0]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=term)
        df_lst.append(data)
    return df_lst

# Main bulk of categorical features
# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
# List of scores as df
lst_df = produce_df_lst_v2(sl_orig, DATA_FOLDER)
# Makes df with scores
df_orig = pd.concat(lst_df, axis=0)
df_orig = df_orig.set_index('class_label')

# List of scores files
sl_orig2 = get_scores_lst(TTI_FOLDER)
# List of scores as df
lst_df2 = produce_df_lst_v2(sl_orig2, TTI_FOLDER)
# Makes df with scores
df_orig2 = pd.concat(lst_df2, axis=0)
df_orig2 = df_orig2.set_index('class_label')

new_df = pd.concat([df_orig, df_orig2], axis=0)
new_df.to_csv(OUTPUT, sep='\t')