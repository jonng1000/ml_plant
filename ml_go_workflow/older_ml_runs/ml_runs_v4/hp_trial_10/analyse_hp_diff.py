# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:43:53 2021

@author: weixiong001

Processes hp tests results into a format which is convenient for plotting.
Different from analyse_hp.py as this counts each set of parameters as one
group, instead of splitting up and counting each parameter individually
"""
import os
import pandas as pd

FOLDER = './results/'
OUTPUT = 'all_hp_counts_diff.txt'

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
high_score = high_score.astype(str)
med_score = sorted_df_hp.loc[(sorted_df_hp['mean_test_score'] < 0.7) & 
                             (sorted_df_hp['mean_test_score'] >= 0.5), 
                             ['param_rf__n_estimators', 
                              'param_rf__max_features', 
                              'param_rf__max_depth',
                              'param_rf__ccp_alpha',
                              'mean_test_score']
                             ]
med_score = med_score.astype(str)
low_score = sorted_df_hp.loc[(sorted_df_hp['mean_test_score'] < 0.5), 
                             ['param_rf__n_estimators', 
                              'param_rf__max_features', 
                              'param_rf__max_depth',
                              'param_rf__ccp_alpha',
                              'mean_test_score']
                             ]
low_score = low_score.astype(str)

high_counts = high_score.groupby(['param_rf__n_estimators',
                                  'param_rf__max_features',
                                  'param_rf__max_depth', 'param_rf__ccp_alpha'
                                  ]).size().reset_index()
high_counts = high_counts.sort_values(by=[0, 'param_rf__n_estimators',
                                         'param_rf__max_features',
                                         'param_rf__max_depth',
                                         'param_rf__ccp_alpha'], ascending=False)
med_counts = med_score.groupby(['param_rf__n_estimators',
                                 'param_rf__max_features',
                                 'param_rf__max_depth', 'param_rf__ccp_alpha',
                                 ]).size().reset_index()
med_counts = med_counts.sort_values(by=[0, 'param_rf__n_estimators',
                                        'param_rf__max_features',
                                        'param_rf__max_depth',
                                        'param_rf__ccp_alpha'], ascending=False)
low_counts = low_score.groupby(['param_rf__n_estimators',
                                 'param_rf__max_features',
                                 'param_rf__max_depth', 'param_rf__ccp_alpha',
                                 ]).size().reset_index()
low_counts = low_counts.sort_values(by=[0, 'param_rf__n_estimators',
                                        'param_rf__max_features',
                                        'param_rf__max_depth',
                                        'param_rf__ccp_alpha'], ascending=False)

high_counts.insert(0, column='score', value='high')
med_counts.insert(0, column='score', value='med')
low_counts.insert(0, column='score', value='low')

all_tgt = pd.concat([high_counts, med_counts, low_counts])
all_tgt = all_tgt.rename({0: 'count'}, axis='columns')
all_tgt.index.name = 'id'
all_tgt.to_csv(OUTPUT, sep='\t')

# This shows that the most freq hps from analyse_hp.py, occurs here when hp
# are grouped into their respective sets
best_params = high_counts.loc[(high_counts['param_rf__ccp_alpha'] == '0.001') & 
                              (high_counts['param_rf__max_depth'] == 'nan') &
                              (high_counts['param_rf__max_features'] == '0.4') &
                              (high_counts['param_rf__n_estimators'] == '200'), 
                              :]
med_params = med_counts.loc[(med_counts['param_rf__ccp_alpha'] == '0.001') & 
                             (med_counts['param_rf__max_depth'] == 'nan') &
                             (med_counts['param_rf__max_features'] == '0.4') &
                             (med_counts['param_rf__n_estimators'] == '200'), 
                             :]
low_params = low_counts.loc[(low_counts['param_rf__ccp_alpha'] == '0.001') & 
                            (low_counts['param_rf__max_depth'] == 'nan') &
                            (low_counts['param_rf__max_features'] == '0.4') &
                            (low_counts['param_rf__n_estimators'] == '200'), 
                            :]
