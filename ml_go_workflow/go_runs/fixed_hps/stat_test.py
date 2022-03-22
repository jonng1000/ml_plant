# -*- coding: utf-8 -*-
"""
Created on Thu May 27 17:59:13 2021

@author: weixiong001

Does Mann–Whitney U test to see if there is a statistically significant
difference between GO class sizes between score groups
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

DATA_FOLDER = './output4/'
GO_COUNTS = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'

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

high = combined_df.loc[combined_df['oob_f1'] >= 0.7, :]
not_high = combined_df.loc[~(combined_df['oob_f1'] >= 0.7), :]

'''
# Number of GO classes in each of these grps
high.shape
Out[68]: (99, 8)
not_high.shape
Out[69]: (1280, 8)
'''

#######################################################################
# Test to see if there is a statistically significant difference
# between GO class sizes of the high and not high scoring grp

# By default, gives half the p-value of the two tailed test, not sure
# exactly what this is, but just ignore it
mannwhitneyu(high['Counts'], not_high['Counts'])
# MannwhitneyuResult(statistic=44416.5, pvalue=3.449613501230544e-07)

# Two tailed test, to see if x is different from y, this is the test which
# I typically want to run
mannwhitneyu(high['Counts'], not_high['Counts'], alternative='two-sided')
# MannwhitneyuResult(statistic=82303.5, pvalue=6.899227002461088e-07)

# One tailed test, to see if x is < y
mannwhitneyu(high['Counts'], not_high['Counts'], alternative='less')
# MannwhitneyuResult(statistic=82303.5, pvalue=0.9999996555040761)

# One tailed test, to see if x is > y
mannwhitneyu(high['Counts'], not_high['Counts'], alternative='greater')
# MannwhitneyuResult(statistic=82303.5, pvalue=3.449613501230544e-07)
#######################################################################

#######################################################################
# Test to see if there is a statistically significant difference
# between GO class sizes of the top 50 and bot 50 scoring GO class
sorted_df = combined_df.sort_values(by='oob_f1', ascending=False)
top_50 = sorted_df.iloc[:50, :]
bot_50 = sorted_df.iloc[-50:, :]

# Two tailed test, to see if x is different from y, this is the test which
# I typically want to run
mannwhitneyu(top_50['Counts'], bot_50['Counts'], alternative='two-sided')
# MannwhitneyuResult(statistic=2034.0, pvalue=6.441953010618085e-08)

