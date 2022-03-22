# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:29:25 2021

@author: weixiong001

Compiles all continuous features scores, remove those 54 mislabelled 
ttr_cluster ids, should be tti_cluster
"""
import pandas as pd
import os
import csv


DATA_FOLDER = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/output/'
MAP_DOC = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
OUTPUT = 'edited_contf_scores.txt'

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

# Mapping dictionary to convert my placeholder names for continuous features
# back to their original names
map_dict = {}
with open(MAP_DOC, newline='') as csvfile:
    creader = csv.reader(csvfile, delimiter='\t')
    for row in creader:
        map_dict[row[1]] = row[0]
    
temp = df_orig.reset_index()
temp.replace({'class_label': map_dict}, inplace=True)
new_df = temp.set_index('class_label')
# Removing 54 mislabelled ttr_cluster ids, should be ttf_cluster
edited = new_df.loc[~new_df.index.str.startswith('ttr_cluster_id'), :]

edited.to_csv(OUTPUT, sep='\t')
