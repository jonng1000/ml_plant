# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:43:53 2021

@author: weixiong001

Processes hp tests results into a format which is convenient for plotting
"""
import os
import pandas as pd

FOLDER = './output_hp/'
OUTPUT = 'all_hp_counts.txt'

df_lst = []
for one in os.listdir(FOLDER):
    if '_hp' in one:
        file_path = FOLDER + one
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        df_selected = data.loc[:, ['mean_fit_time', 'mean_score_time', 
                                   'param_rf__n_estimators',
                                   'param_rf__max_features', 
                                   'param_rf__max_depth',
                                   'param_rf__ccp_alpha', 'mean_test_score']
                               ]
        df_lst.append(df_selected)

df_hp = pd.concat(df_lst, axis=0)
sorted_df_hp = df_hp.sort_values(by=['mean_test_score'], ascending=False)
all_tgt = sorted_df_hp.reset_index(drop=True)
all_tgt.index.name = 'id'
all_tgt.to_csv(OUTPUT, sep='\t')