# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:43:53 2021

@author: weixiong001

Processes hp tests results into a format which is convenient for plotting
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

high_reset = high_melt.value_counts().reset_index()
med_reset = med_melt.value_counts().reset_index()
low_reset = low_melt.value_counts().reset_index()

high_reset.insert(0, column='score', value='high')
med_reset.insert(0, column='score', value='med')
low_reset.insert(0, column='score', value='low')

all_tgt = pd.concat([high_reset, med_reset, low_reset])
all_tgt = all_tgt.rename({0: 'count'}, axis='columns')
all_tgt.index.name = 'id'
all_tgt.to_csv(OUTPUT, sep='\t')