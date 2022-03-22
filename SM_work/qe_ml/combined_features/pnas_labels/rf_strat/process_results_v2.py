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
freq_params.sort_values('Freq', axis=0, ascending=False)
#Out[57]: 
#   criterion  max_features  n_estimators  Freq
#19      gini             3            50     8
#18      gini             2           800     8
#0    entropy             2            50     7
#4    entropy             2           800     6
#2    entropy             2           300     5
#7    entropy             3           300     5
#11   entropy             4           300     5
#1    entropy             2           100     4
#3    entropy             2           500     4
#6    entropy             3           100     4
#25      gini             4           100     4
#17      gini             2           500     4
#26      gini             4           300     3
#23      gini             3           800     3
#14      gini             2            50     3
#10   entropy             4            50     3
#9    entropy             3           800     3
#8    entropy             3           500     3
#15      gini             2           100     2
#16      gini             2           300     2
#13   entropy             4           800     2
#20      gini             3           100     2
#24      gini             4            50     2
#5    entropy             3            50     2
#28      gini             4           800     2
#12   entropy             4           500     1
#21      gini             3           300     1
#22      gini             3           500     1
#27      gini             4           500     1

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
scores_df['tpr'].mean()
#Out[37]: 0.6802380952380951
scores_df['tnr'].mean()
#Out[66]: 0.8427692307692313