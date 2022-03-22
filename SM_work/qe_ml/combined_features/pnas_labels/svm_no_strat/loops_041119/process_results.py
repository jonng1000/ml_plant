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


holding_list = []
for filename in os.listdir('./conf_matrix'):
    cm_df = pd.read_csv('./conf_matrix/' + filename, sep="\t", index_col=0)
    tn, fp, fn, tp = cm_df.values.ravel()
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    holding_list.append([tpr, tnr])

all_scores = pd.DataFrame(holding_list, columns = ['TPR', 'TNR'])
# Results, not very good
#all_scores['TPR'].mean()
#Out[37]: 0.3664444444444442
#
#all_scores['TNR'].mean()
#Out[38]: 0.9747244094488192