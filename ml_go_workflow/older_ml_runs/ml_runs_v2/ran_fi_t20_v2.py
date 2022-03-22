# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:01 2020

@author: weixiong001

Get mean feature importances for all 16 cellular locations, selects
top 20 from them, and saves it to a file, based on plots_fi.py
"""
import os
import pandas as pd


DATA_FOLDER = './results_ran/'
OUTPUT = 'top20_fi_ran.txt'

# Gets list of feature importance files
all_files = [a_file for a_file in os.listdir(DATA_FOLDER)]
fi_list = [one for one in all_files if one.endswith('_fi.txt')]
# Selects only random forest feature importance files
selected = []
for one_file in fi_list:
    if one_file.startswith('rf'):
        selected.append(one_file)
# Create dataframe from random forest's feature importance
df_lst = []
for one in selected:
    file_path = DATA_FOLDER + '/' + one
    # model name
    model_name = one.split('_')[0]
    # Reads in dataset, takes ~1 min
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    # Insert is in place
    data.insert(loc=0, column='model_name', value=model_name)
    df_lst.append(data)

df = pd.concat(df_lst, axis=1)
cell_loc = {name for name in df.columns if name.endswith('_importance')}
# Getting dataframe of top 20 mean feature importance
series_lst = []
for one_loc in cell_loc:
    one_loc_fi = df.loc[:, one_loc].copy()
    one_loc_fi.columns = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5']
    one_loc_fi['mean'] = one_loc_fi.mean(axis=1)
    sorted_fi = one_loc_fi.sort_values(['mean'], ascending=False)
    top = sorted_fi.iloc[:20, :]
    top.reset_index()
    top = top.reset_index()
    values20 = top.loc[:, 'mean'].copy()
    values20.name = one_loc.split('_ran')[0]
    series_lst.append(values20)

top20_df = pd.concat(series_lst, axis=1)
top20_df.index.name = 'id'
top20_df.to_csv(OUTPUT, sep='\t')
