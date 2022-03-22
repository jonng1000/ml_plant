# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Visualises distributions of oob R^2 scores of continuous features, those which
scored well and those which did not.

Modified from visualise_boxplot_scores.py in
D:\GoogleDrive\machine_learning\ml_go_workflow\go_runs
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

DATA_FOLDER = './output/'
FIG = 'combined_boxplot.png'


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

# This section is for plotting
# To ensure my plotting code can run
data_used = df_orig

g = sns.boxplot(y=data_used['oob_r_sq'])
g.set(xlabel='Continuous features')
g.figure.savefig(FIG)
plt.close()
