# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:08:51 2021

@author: weixiong001

Explore scores from ml workflow
Saves high scoring features to a file
"""

import os
import numpy as np
import pandas as pd

DATA_FOLDER = './output/'
OUTPUT = 'high_dge_features.txt'
OUTPUT2 = 'score04_dge_features.txt'

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
    for one in sl_orig:
        file_path = DATA_FOLDER + '/' + one
        term = one.split('_scores')[0]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=term)
        df_lst.append(data)
    return df_lst


# List of scores files
sl_orig = get_scores_lst(DATA_FOLDER)
# List of scores as df
lst_df = produce_df_lst_v2(sl_orig, DATA_FOLDER)
# Makes df with scores
df_orig = pd.concat(lst_df, axis=0)
df_orig = df_orig.set_index('class_label')

high = df_orig.loc[df_orig['oob_f1'] >= 0.7, :]
at_least_avg = df_orig.loc[df_orig['oob_f1'] >= 0.5, :]
thresh_04 = df_orig.loc[df_orig['oob_f1'] >= 0.4, :]

labels = high.reset_index().loc[:, 'class_label']
labels.index.name = 'id'
labels.to_csv(OUTPUT, sep='\t', index=False)

labels04 = thresh_04.reset_index().loc[:, 'class_label']
labels04.index.name = 'id'
labels04.to_csv(OUTPUT2, sep='\t', index=False)