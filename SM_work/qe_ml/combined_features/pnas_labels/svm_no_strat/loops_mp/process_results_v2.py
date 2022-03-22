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
#freq_params.groupby(list(freq_params.columns)).size().reset_index()
#Out[64]: 
#      C    gamma  kernel  Freq  0
#0     1  0.00001  linear     1  1
#1    10  0.00001  linear     8  1
#2   100  0.00001  linear     9  1
#3   100  0.01000     rbf     3  1
#4  1000  0.00001  linear     6  1
#5  1000  0.00100     rbf     2  1
#6  1000  0.01000     rbf    71  1

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.5843750000000008
scores_df['tnr'].mean()
#Out[66]: 0.8324193548387088