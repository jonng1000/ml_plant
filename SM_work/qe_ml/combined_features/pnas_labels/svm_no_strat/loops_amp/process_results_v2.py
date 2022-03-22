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
#params_df.groupby(list(params_df.columns)).size().reset_index()
#Out[3]: 
#           C    gamma  kernel   0
#0       0.01  0.00001  linear  49
#1       1.00  0.00001  linear   2
#2      10.00  0.00001  linear   1
#3     100.00  0.00001  linear   1
#4     100.00  0.01000     rbf  21
#5    1000.00  0.00001  linear   1
#6    1000.00  0.00100     rbf   2
#7   10000.00  0.00001  linear   1
#8   10000.00  0.00001     rbf   1
#9   10000.00  0.00010     rbf   2
#10  10000.00  0.00100     rbf  19

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.554285714285714
scores_df['tnr'].mean()
#Out[66]: 0.8891056910569098