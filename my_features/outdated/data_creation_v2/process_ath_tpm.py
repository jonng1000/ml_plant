# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis gene expression from Irene
and does very simple preprocessing (data is already quite clean)
before saving it as a new file. Edited from process_ath_exp.py
in /mnt/d/GoogleDrive/machine_learning/my_features/data_preprocessing
"""

import pandas as pd
from scipy.stats import median_absolute_deviation

FILE = 'Ath_matrix.av'
OUTPUT = 'edited_Ath_tpm.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.index.name = 'Gene'
df.rename(mapper=lambda x: 'tpm_' + x, axis='columns', inplace=True)

mean_df = df.mean(axis=1)
median_df = df.median(axis=1)
max_df =  df.max(axis=1)
min_df =  df.min(axis=1)
var_df = df.var(axis=1)
mad_df = median_absolute_deviation(df, axis=1)/median_df

df['tpm_mean'] = mean_df
df['tpm_median'] = median_df
df['tpm_max'] = max_df
df['tpm_min'] = min_df
df['tpm_var'] = var_df
df['tpm_mad'] = mad_df

selected_feat = df.loc[:, ['tpm_mean', 'tpm_median', 'tpm_max',
                           'tpm_min', 'tpm_var','tpm_mad']
                       ]

# Basic looking through the data
'''
# Number of cells in dataframe
>>> df.size
327572
# Missing values in dataframe
>>> df.isnull().values.any()
True
# Finding origin of missing values
df.isnull().any()
Out[53]: 
tpm_Flowers           False
tpm_Seeds/Spores      False
tpm_Meristem          False
tpm_Leaves/Thallus    False
tpm_Roots             False
tpm_Male              False
tpm_Stems             False
tpm_Female            False
tpm_mean              False
tpm_median            False
tpm_max               False
tpm_min               False
tpm_var               False
tpm_mad                True
dtype: bool
# Reason why there is nan in tpm_mad, since median is 0 for all of
# them
df['tpm_median'].loc[df['tpm_mad'].isnull()].unique()
Out[58]: array([0.])
'''
selected_feat.to_csv(OUTPUT, sep='\t')
