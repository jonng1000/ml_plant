# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:12:33 2019

@author: weixiong001

Need raw outputs to be in a different folder, so that when rerunning the
script, the output of the script will not cause bugs, as its name will be
simlar to the raw outputs.
"""
import os
import pandas as pd

source = './raw_output/'

results = []
scores = []
for file in os.listdir(source):
    if 'results.csv' in file:
        name = file.split('_')[0]
        df = pd.read_csv(source + file, sep="\t", index_col=0).reset_index()
        df.insert(0, 'ml', [name]*len(df))
        results.append(df)
    elif 'scores.csv' in file:
        name = file.split('_')[0]
        df = pd.read_csv(source + file, sep="\t", index_col=0).reset_index()
        df.insert(0, 'ml', [name]*len(df))
        scores.append(df)


df_results = pd.concat(results).reset_index(drop=True)
df_results.rename(columns={"index": "result_type"}, inplace=True)
df_scores = pd.concat(scores).reset_index(drop=True)

df_results.to_csv('combined_results.csv', sep='\t')
df_scores.to_csv('combined_scores.csv', sep='\t')
