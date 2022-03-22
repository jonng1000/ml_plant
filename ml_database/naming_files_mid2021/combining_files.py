# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 17:54:07 2021

@author: weixiong001

Combine all the feature names into one file for easy downstream work
"""

import os
import pandas as pd

PATH = './'
OUTPUT = 'combined_names.txt'

selected_files = []
for file in os.listdir():
    if '_info' in file:
        selected_files.append(file)
        
selected_df = []
for file in selected_files:
    df = pd.read_csv(file, sep='\t', index_col=0)
    selected_df.append(df)
    
all_df = pd.concat(selected_df)

all_df.to_csv(OUTPUT, sep='\t')