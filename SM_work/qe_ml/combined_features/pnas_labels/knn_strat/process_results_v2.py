# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:15:58 2019

@author: weixiong001

This script is to process results from running gridsearch and SVM model
100 times. Finds average true positve rate and true negative rate from
all runs. Called v2 as it uses a different input from process_results,
it just needs all_scores.csv to analysse the scores.
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns

params_df = pd.read_csv("params_matrix.csv", sep="\t", index_col=0)
freq_params = params_df.groupby(list(params_df.columns)).size().reset_index()
freq_params.rename(columns={0: "Freq"}, inplace=True)
freq_params
#Out[31]: 
#    leaf_size  n_neighbors  p   weights  Freq
#0           3            3  2  distance     1
#1           3            3  4  distance     2
#2           3            3  4   uniform     4
#3           3            3  5  distance     2
#4           3            5  1   uniform    14
#5           3            5  2   uniform     4
#6           3            5  3  distance     1
#7           3            5  3   uniform     3
#8           3            5  4   uniform     6
#9           3            5  5  distance     1
#10          3            5  5   uniform     8
#11          3            7  1   uniform    30
#12          3            7  2   uniform     4
#13          3            7  3  distance     3
#14          3            7  3   uniform     1
#15          3            9  1  distance     5
#16          3            9  1   uniform     5
17          3           11  1  distance     6

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.6566666666666667
scores_df['tnr'].mean()
#Out[66]: 0.8448461538461537