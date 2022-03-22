# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:47:33 2020

@author: weixiong001
"""

import pandas as pd
import os

STARTER_FILE = 'cytosol_GO.txt'
OUTPUT_FILE = 'combined_marek.txt'

def get_ohe_cl(one_file):
    """
    This function takes a dataframe, one_file, converts class labels
    into 1s and 0s for positive and negative classes respectively,
    renames it to whatever the class labels means,
    and returns just the class labels as a dataframe with 1s and 0s
    """
    df = pd.read_csv(one_file, sep='\t', index_col=0)
    new_label = 'go_' + one_file.split('_GO')[0]
    pos_class = one_file.split('_GO')[0].replace('_', ' ')
    neg_class = 'not ' + one_file.split('_GO')[0].replace('_', ' ')
    
    df.rename(columns={'AraCyc annotation': new_label}, inplace=True)
    df[new_label].replace({pos_class: 1, neg_class: 0}, inplace=True)
    ohe_cl = df.loc[:, new_label].to_frame()
    return ohe_cl

# Loads in a starter file, can be any of the GO dataset, to
# extract core data without class labels
df = pd.read_csv(STARTER_FILE, sep='\t', index_col=0)
core_df = df.drop(['AraCyc annotation'], axis=1)
lst_labels = [core_df]
# Iterates through all files in folders, selects GO dataset, and
# calls  get_ohe_cl(one_file) to encode and extract class labels
# as a dataframe with one column. Appends these to a list containing
# core dataset and all encoded class labels
for file in os.listdir():
    if file.endswith('_GO.txt'):
        class_label = get_ohe_cl(file)
        lst_labels.append(class_label)
# Combines all dataframe in a list, and writes it to a .txt file
combined_df = pd.concat(lst_labels, axis=1)
combined_df.to_csv(OUTPUT_FILE, sep='\t')
