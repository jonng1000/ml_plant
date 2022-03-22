# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Edited from fully_proc.py
Takes partially processed output from dtypes_partial_proc.py and does
- replace all class labels with nan
- one hot encodes categorical features using pandas, not sklearn
- produces file which can be directly used for machine learning

Generates 100 random continous and categorical variables
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

file = 'D:/GoogleDrive/machine_learning/RF_PNAS/partial_processed.txt'
category_file = 'D:/GoogleDrive/machine_learning/RF_PNAS/cat_features.txt'
suba = 'Suba4-2020-3-9_15-43.csv'

df = pd.read_csv(file, sep='\t', index_col=0)
cat_features = pd.read_csv(category_file, sep='\t', index_col=0)
df.loc[:, cat_features['0']] = df.loc[:, cat_features['0']].astype('category')

suba_df = pd.read_csv(suba, sep=',', index_col=0)
# Checked to make sure all genes are unique, they are
suba_df.rename(index=lambda s: s.split('.')[0], inplace=True)
suba_set = set(suba_df.index)
df_set = set(df.index)

# subs genes are a subset of my main df genes, but some of these genes are not
# in suba
# suba_set - df_set
# Out[71]: set()

# df_set - suba_set
# Out[72]: 
# {'AT1G45231',
#  'AT4G00520',
#  'AT4G03060',
#  'AT4G03060-CVI',
#  'AT4G32700',
#  'AT5G54130'}

df['suba'] = suba_df['location_consensus']
df.drop(list(df_set - suba_set), inplace=True)
df['AraCyc annotation'] = np.nan

# Created as a list,but will be converted to a set later
master_set = []
for x in set(suba_df['location_consensus']):
    temp_l = x.split(',')
    if len(temp_l) == 1:
        master_set.append(temp_l[0])
    else:
        master_set.extend(temp_l)
master_set = set(master_set)

# Set of suba predictions
# master_set
# Out[10]: 
# {'cytosol',
#  'endoplasmic reticulum',
#  'extracellular',
#  'golgi',
#  'mitochondrion',
#  'nucleus',
#  'peroxisome',
#  'plasma membrane',
#  'plastid',
#  'vacuole'}

for pred in master_set:
    df[pred] = df['suba'].str.contains(pred, regex=False).astype('int32')
df.drop(columns=['suba'], inplace=True)

for i in range(1, 101):
    df['cont_' + str(i)] = np.random.random(size = len(df))
    df['cat_' + str(i)] = np.random.randint(2, size = len(df))

# Onehotencoding can't be used with nan values
df = pd.get_dummies(df)

# Predictions from suba are coded as int32 datatypes
# df.dtypes.astype(str).value_counts()
# Out[133]: 
# int64      4806
# uint8      4674
# float64      61
# int32        10
# dtype: int64

# This dataset has no nan except for class labels, has categorical values
# coded as dummy variables

df.to_csv('fully_processed_suba.txt', sep='\t', na_rep='nan')

