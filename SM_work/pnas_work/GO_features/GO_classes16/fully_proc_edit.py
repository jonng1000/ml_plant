# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Edited from fully_proc.py
Takes partially processed output from dtypes_partial_proc.py and does
- replace all class labels with nan
- one hot encodes categorical features using pandas, not sklearn
- produces file which can be directly used for machine learning
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

file = 'D:/GoogleDrive/machine_learning/RF_PNAS/partial_processed.txt'
category_file = 'D:/GoogleDrive/machine_learning/RF_PNAS/cat_features.txt'

df = pd.read_csv(file, sep='\t', index_col=0)
cat_features = pd.read_csv(category_file, sep='\t', index_col=0)
df.loc[:, cat_features['0']] = df.loc[:, cat_features['0']].astype('category')

# df.dtypes.astype(str).value_counts()
# int64       4806
# category      65
# float64       60
# object         1
# dtype: int64

df['AraCyc annotation'] = np.nan

# df['AraCyc annotation'].value_counts(dropna=False)
# All is nan

# Before creating dummy variables, 4932 features
# df.shape
# Out[3]: (5251, 4932)

# Onehotencoding can't be used with nan values
#df = pd.get_dummies(df)

# After creating dummy variables, 9538 features
# df.shape
# Out[6]: (5251, 9538)

# This dataset has no nan except for class labels, has categorical values
# coded as dummy variables

# df.to_csv('fully_processed_edited.txt', sep='\t', na_rep='nan')
