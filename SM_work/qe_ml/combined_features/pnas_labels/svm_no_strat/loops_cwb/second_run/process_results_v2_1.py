# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:15:58 2019

@author: weixiong001

This script is to process results from running gridsearch and SVM model
100 times. Finds average true positve rate and true negative rate from
all runs. Called v2_1 as it uses a slightly different input from process_results_v2.
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns

params_df = pd.read_csv("params_matrix.csv", sep="\t", index_col=0)
freq_params = params_df.groupby(list(params_df.columns)).size().reset_index()
freq_params.rename(columns={0: "Freq"}, inplace=True)
#freq_params
#Out[64]: 
#   C  gamma kernel    0
#0  1  0.001    rbf  100

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0, header=None)
# Results, not very good