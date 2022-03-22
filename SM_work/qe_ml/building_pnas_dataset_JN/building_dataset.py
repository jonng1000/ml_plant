# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:08:59 2019

@author: weixiong
This script takes individual .txt files (each a dataset) and combines them
to form one big dataframe - contains features for genes

Each code block here should be run one after the other
"""

import os
import pandas as pd

# =============================================================================
# Performs the operation to combines dataframe
empty_df = pd.DataFrame()
first = True
for file in os.listdir():
    if file.startswith('d2'):
        if first:
            dataset = pd.read_csv(file, sep='\t', index_col=0)
        else:
            dataset2 = pd.read_csv(file, sep='\t', index_col=0)
            dataset = dataset.join(dataset2, how='outer')
        first = False

dataset.index.name = 'Gene'
#dataset.to_csv("combined_data.txt", sep='\t', na_rep='NA')
# =============================================================================

# =============================================================================
# Just to check files' characteristics, after running above
combined_dataset = pd.read_csv('combined_data.txt', sep='\t', index_col=0)
#combined_dataset.shape #(5239, 4362), 5239 genes, 4362 features

shape_list = []
for file in os.listdir():
    if file.startswith('d2'):
        dataset = pd.read_csv(file, sep='\t', index_col=0)
        shape_list.append([file, dataset.shape])
        
cols = [x[1][1] for x in shape_list]
#sum(cols) #4362
# =============================================================================
