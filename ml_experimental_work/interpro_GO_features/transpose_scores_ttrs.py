# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:17:49 2022

@author: weixiong001
"""
import pandas as pd
import numpy as np
import os

FOLDER = './output_ttrs/'

orig_files = [FOLDER + a_file for a_file in os.listdir(FOLDER)]
    
for a_file in orig_files:
    new_file = './output_ttrs_edited/' + a_file.split('/')[2]
    data = pd.read_csv(a_file, sep='\t', header=None, index_col=None)
    dropped = data.drop(0)
    dfs = np.array_split(dropped, 30)
    transposed_dfs = []
    for one in dfs:
        temp = one.T
        temp.columns = temp.iloc[0]
        dropped = temp.drop(0)
        transposed_dfs.append(dropped)
    
    df_scores = pd.concat(transposed_dfs, axis=0)
    df_scores.reset_index(drop=True, inplace=True)
    df_scores.index.name = 'id'
    df_scores.to_csv(new_file, sep='\t')