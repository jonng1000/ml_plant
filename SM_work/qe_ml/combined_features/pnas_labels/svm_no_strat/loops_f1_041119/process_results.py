# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:15:58 2019

@author: weixiong001

This script is to process results from running gridsearch and SVM model
100 times. Finds average true positve rate and true negative rate from
all runs.
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns

params_df = pd.read_csv("params_matrix.csv", sep="\t", index_col=0)
freq_params = params_df.groupby(list(params_df.columns)).size().reset_index()
freq_params.rename(columns={0: "Freq"}, inplace=True)
#freq_params.groupby(list(freq_params.columns)).size().reset_index()
#Out[61]: 
#      C  gamma  kernel  Freq  0
#0   0.1  0.001  linear     3  1
#1   1.0  0.001  linear     9  1
#2   1.0  0.010     rbf     1  1
#3   1.0  0.100     rbf    22  1
#4  10.0  0.001  linear    48  1
#5  10.0  0.001     rbf     1  1
#6  10.0  0.010     rbf     8  1
#7  10.0  0.100     rbf     8  1

holding_list = []
for filename in os.listdir('./conf_matrix'):
    cm_df = pd.read_csv('./conf_matrix/' + filename, sep="\t", index_col=0)
    tn, fp, fn, tp = cm_df.values.ravel()
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    holding_list.append([tpr, tnr])

all_scores = pd.DataFrame(holding_list, columns = ['TPR', 'TNR'])
# Results, better compared to when grid search is set to precision
all_scores['TPR'].mean()
#Out[37]: 0.6154545454545465
#
all_scores['TNR'].mean()
#Out[38]: 0.8453125