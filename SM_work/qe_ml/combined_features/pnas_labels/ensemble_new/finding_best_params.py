# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:15:58 2019

@author: weixiong001

This script is to process results from running gridsearch and all models
100 times. Finds best params for each model
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns

source = './raw_output/'

params = []
to_use = [file for file in os.listdir(source) if 'params_matrix' in file]

for f in to_use:
    name = f.split('_')[0]
    params_df = pd.read_csv(source + f, sep="\t", index_col=0)
    freq_params = params_df.groupby(list(params_df.columns)).size().reset_index()
    freq_params.rename(columns={0: "Freq"}, inplace=True)
    # Need to do this since there are many combinations of hyperparameters
    freq_params.sort_values('Freq', axis=0, ascending=False, inplace=True)
    freq_params.to_csv(name + '_freq_params.csv', sep='\t')