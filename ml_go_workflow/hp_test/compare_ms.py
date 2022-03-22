# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

This is to check to see if the GO classes used for my hp test, contains the 16
classes which marek has selected previously, but it does not, so did not
proceed with plotting here. Originally, I wanted to plot the scores for these
16 classes, with and without hp optimisation
"""

import os
import pandas as pd

DATA_FOLDER = './results/'
DATA_FOLDER2 = './results_dhp/'
MAREK_SELECT = 'D:/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'

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

ms = pd.read_csv(MAREK_SELECT, sep='\t', header=None)
ms.rename(columns={0: 'GO_class'}, inplace=True)
ms.loc[:, 'GO_class'] = ms['GO_class'].str.replace(':','_')

combined_df = pd.concat([opt_hp, d_hp], axis=0)
# Sorts by class_label, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('class_label')
