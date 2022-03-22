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
#freq_params
#Out[3]: 
#      C  gamma  kernel  Freq
#0  0.01  0.001  linear   100

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.30303030303030365
scores_df['tnr'].mean()
#Out[66]: 0.9856115107913681