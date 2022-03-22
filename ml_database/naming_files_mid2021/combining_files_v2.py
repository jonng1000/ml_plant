# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 17:54:07 2021

@author: weixiong001

Combine all the feature names into one file for easy downstream work.
Modified from combining_files.py in
D:/GoogleDrive/machine_learning/ml_database
"""

import os
import pandas as pd

PATH = './'
OUTPUT = 'combined_names_v2.txt'

selected_files = []
for file in os.listdir():
    if '_info' in file:
        # This file is outdated so ignores it
        if file == 'ath_ttr_clusters_info.txt':
            continue
        selected_files.append(file)

selected_df = []
for file in selected_files:
    df = pd.read_csv(file, sep='\t', index_col=0)
    selected_df.append(df)
    
all_df = pd.concat(selected_df)

all_df.to_csv(OUTPUT, sep='\t')
