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

FILE = 'ARATH.tpm.av'
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
360660
# Missing values in dataframe
>>> df.isnull().values.any()
True
# Finding origin of missing values
df.isnull().any()
Out[53]: 
tpm_Stem               False
tpm_Female             False
tpm_Leaf               False
tpm_Flower             False
tpm_Male               False
tpm_Seeds              False
tpm_Root               False
tpm_Apical meristem    False
tpm_Root meristem      False
tpm_mean               False
tpm_median             False
tpm_max                False
tpm_min                False
tpm_var                False
tpm_mad                 True
dtype: bool
# Reason why there is nan in tpm_mad, since median is 0 for all of
# them
df['tpm_median'].loc[df['tpm_mad'].isnull()].unique()
Out[58]: array([0.])
'''
selected_feat.to_csv(OUTPUT, sep='\t')

'''
selected_feat
Out[123]: 
             tpm_mean  tpm_median  ...       tpm_var   tpm_mad
Gene                               ...                        
AT1G06620   33.608617   14.343470  ...   3503.290839  0.969948
AT5G08160   48.789566   41.412672  ...    545.974494  0.137951
AT4G22890   53.596056   41.317013  ...   2310.962376  1.296033
AT5G54067    1.907046    0.021655  ...     30.920069  1.482600
AT2G34630   28.281680   24.552760  ...    104.896573  0.287653
              ...         ...  ...           ...       ...
AT3G58660   81.383182   83.914359  ...   3621.519470  0.705061
AT3G50410   61.359994    9.173650  ...  25224.284887  1.369320
AT5G64080  153.275226  101.439341  ...  18139.725688  1.169252
AT1G09470   11.034569    9.253061  ...     92.355687  0.689827
AT1G76900   40.315290   21.692095  ...   2779.318075  0.286341

[24044 rows x 6 columns]
'''
