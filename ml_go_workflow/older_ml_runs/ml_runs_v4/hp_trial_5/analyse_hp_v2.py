# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:43:53 2021

@author: weixiong001

Processes hp tests results into a format which is convenient for plotting.
Improved version of analyse_hp.py located in
D:/GoogleDrive/machine_learning/ml_go_workflow/ml_runs_v4/hp_trial_5
Fixed the bug where lineplot does not show x-axis labels in the correct order,
probably because float values are not easily compared, so in future, need to check this
"""
import os
import pandas as pd

FOLDER = './results/'
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
high_score = sorted_df_hp.loc[(sorted_df_hp['mean_test_score'] >= 0.7), 
                              ['param_rf__n_estimators', 
                               'param_rf__max_features', 
                               'param_rf__max_depth',
                               'param_rf__ccp_alpha',
                               'mean_test_score']
                              ]
med_score = sorted_df_hp.loc[(sorted_df_hp['mean_test_score'] < 0.7) & 
                             (sorted_df_hp['mean_test_score'] >= 0.5), 
                             ['param_rf__n_estimators', 
                              'param_rf__max_features', 
                              'param_rf__max_depth',
                              'param_rf__ccp_alpha',
                              'mean_test_score']
                             ]
low_score = sorted_df_hp.loc[(sorted_df_hp['mean_test_score'] < 0.5), 
                             ['param_rf__n_estimators', 
                              'param_rf__max_features', 
                              'param_rf__max_depth',
                              'param_rf__ccp_alpha',
                              'mean_test_score']
                             ]

high_melt = pd.melt(high_score, value_vars=['param_rf__n_estimators', 
                                            'param_rf__max_features', 
                                            'param_rf__max_depth',
                                            'param_rf__ccp_alpha'])
med_melt = pd.melt(med_score, value_vars=['param_rf__n_estimators', 
                                            'param_rf__max_features', 
                                            'param_rf__max_depth',
                                            'param_rf__ccp_alpha'])
low_melt = pd.melt(low_score, value_vars=['param_rf__n_estimators', 
                                            'param_rf__max_features', 
                                            'param_rf__max_depth',
                                            'param_rf__ccp_alpha'])

high_melt['value'] = high_melt['value'].astype(str)
high_melt['params'] = high_melt.loc[:, ['variable', 'value']].apply('_'.join, axis=1)
high_reset = high_melt['params'].value_counts().reset_index()

med_melt['value'] = med_melt['value'].astype(str)
med_melt['params'] = med_melt.loc[:, ['variable', 'value']].apply('_'.join, axis=1)
med_reset = med_melt['params'].value_counts().reset_index()

low_melt['value'] = low_melt['value'].astype(str)
low_melt['params'] = low_melt.loc[:, ['variable', 'value']].apply('_'.join, axis=1)
low_reset = low_melt['params'].value_counts().reset_index()

high_reset.insert(0, column='score', value='high')
med_reset.insert(0, column='score', value='med')
low_reset.insert(0, column='score', value='low')

all_tgt = pd.concat([high_reset, med_reset, low_reset])
# Do this twice, as the column name repeats
all_tgt.rename(columns={'params': 'count'}, inplace=True)
all_tgt.rename(columns={'index': 'params'}, inplace=True)
all_tgt.index.name = 'id'
all_tgt.to_csv(OUTPUT, sep='\t')