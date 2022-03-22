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
# Need to do this since there are many combinations of hyperparameters
#freq_params.sort_values('Freq', axis=0, ascending=False)
#Out[12]: 
#   criterion  max_depth  max_features  min_samples_split  Freq
#71      gini        5.0             4                  5     3
#45      gini        1.0             4                  6     2
#39      gini        1.0             3                  5     2
#61      gini        4.0             4                  7     2
#69      gini        4.0             6                 10     2
#..       ...        ...           ...                ...   ...
#31   entropy        5.0             6                  2     1
#30   entropy        5.0             5                  9     1
#29   entropy        5.0             5                  8     1
#27   entropy        5.0             5                  2     1
#84      gini        9.0             3                  9     1
#
#[85 rows x 5 columns]

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.6833333333333331
scores_df['tnr'].mean()
#Out[66]: 0.8215384615384612