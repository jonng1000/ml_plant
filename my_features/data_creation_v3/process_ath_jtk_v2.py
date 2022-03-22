# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis diurnal gene expression from Marek
and extracts statistically significant amplitude and time point features
from it. JTK script used for diurnal gene expression processing. Saves output
to a file

Modified from process_ath_jtk.py in
D:\GoogleDrive\machine_learning\my_features\data_creation_v2
"""

import pandas as pd
import numpy as np

FILE = 'JTK.Ath_Mat.txt'
OUTPUT = 'edited_Ath_jtk.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
# This two lines may not be always essential, but is written to ensure that the
# df index is standardised in the output file, regardless of index in input
# file
# Removes affy probes from dataset
df = df.loc[~df.index.str.startswith('AFF'), :]
df.index = df.index.str.upper()
df.index.name = 'Gene'

selected_df = df.loc[:, ['ADJ.P', 'LAG', 'AMP']].copy()
selected_df.loc[selected_df['ADJ.P'] >= 0.05, 'AMP'] = 0
selected_df.loc[selected_df['ADJ.P'] >= 0.05, 'LAG'] = np.nan

ohe_diu = pd.get_dummies(selected_df, columns=['LAG'], prefix='dit')
ohe_diu.drop(columns=['ADJ.P'], inplace=True)
ohe_diu.rename(columns={'AMP': 'dia_AMP'}, inplace=True)

ohe_diu.to_csv(OUTPUT, sep='\t')
'''
# df dimensions
>>> ohe_diu.shape
(22746, 13)

ohe_diu
Out[100]: 
            dia_AMP  dit_0.0  dit_2.0  ...  dit_18.0  dit_20.0  dit_22.0
Gene                                   ...                              
AT2G30510  1.913891        0        0  ...         0         1         0
AT2G29650  1.824781        0        1  ...         0         0         0
AT5G67030  1.310827        1        0  ...         0         0         0
AT3G01060  1.116119        1        0  ...         0         0         0
AT1G69530  1.049049        0        0  ...         0         1         0
            ...      ...      ...  ...       ...       ...       ...
AT2G32740  0.000000        0        0  ...         0         0         0
AT3G10360  0.000000        0        0  ...         0         0         0
AT4G36460  0.000000        0        0  ...         0         0         0
AT1G64480  0.000000        0        0  ...         0         0         0
AT4G37210  0.000000        0        0  ...         0         0         0

[22746 rows x 13 columns]

# Check to see if any categorical features appear once
ohe_diu.sum()
Out[148]: 
dia_AMP     2558.264096
dit_0.0      310.000000
dit_2.0      292.000000
dit_4.0      378.000000
dit_6.0      858.000000
dit_8.0     1012.000000
dit_10.0     677.000000
dit_12.0     407.000000
dit_14.0     448.000000
dit_16.0     491.000000
dit_18.0     897.000000
dit_20.0     940.000000
dit_22.0     431.000000
dtype: float64
'''