# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Takes partially processed output from dtypes_partial_proc.py and removes
- missing class labels, genes labelled as GM and SM
- one hot encodes categorical features using pandas, not sklearn
- produces file which can be directly used for machine learning
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

file = 'partial_processed.txt'
category_file = 'cat_features.txt'

df = pd.read_csv(file, sep='\t', index_col=0)
cat_features = pd.read_csv(category_file, sep='\t', index_col=0)
df.loc[:, cat_features['0']] = df.loc[:, cat_features['0']].astype('category')

# df.dtypes.astype(str).value_counts()
# int64       4806
# category      65
# float64       60
# object         1
# dtype: int64

# df['AraCyc annotation'].value_counts(dropna=False)
# NaN                                              3258
# Non-secondary metabolism pathway                 1306
# Secondary metabolism pathway                      423
# Seconday and Non-secondary metabolism pathway     264
# Name: AraCyc annotation, dtype: int64

df.dropna(subset=['AraCyc annotation'], inplace=True)

string_remove = 'Seconday and Non-secondary metabolism pathway'
class_label = 'AraCyc annotation'
df = df[df[class_label] != string_remove]

# df.dtypes.astype(str).value_counts()
# Out[119]: 
# int64       4806
# category      65
# float64       60
# object         1
# dtype: int64

# df.isna().sum().sum()
# Out[120]: 14145

# df.select_dtypes(include='float64').isna().sum().sum()
# Out[121]: 0

# df.select_dtypes(include='int64').isna().sum().sum()
# Out[122]: 0

# df.select_dtypes(include='category').isna().sum().sum()
# Out[123]: 14145

# df.select_dtypes(include='object').isna().sum().sum()
# Out[124]: 

# Class labels are represented by the int32 datatype
# df.dtypes.astype(str).value_counts()
# Out[169]: 
# int64       4806
# category      65
# float64       60
# int32          1
# dtype: int64

le = LabelEncoder()
le.fit(df[class_label])
enc = le.transform(df[class_label])
df[class_label] = enc

# le.inverse_transform([0, 1])
# Out[135]: 
# array(['Non-secondary metabolism pathway', 'Secondary metabolism pathway'],
#       dtype=object)

# Onehotencoding can't be used with nan values
df = pd.get_dummies(df)

# After conversion to dummy variables, categorical values represented by the
# uint8 datatype
# df.dtypes.astype(str).value_counts()
# Out[178]: 
# int64      4806
# uint8      4671
# float64      60
# int32         1
# dtype: int64

# pd.get_dummies(df).isna().sum().sum()
# Out[176]: 0

# This dataset has no nan, has categorical values coded as dummy variables

df.to_csv('fully_processed.txt', sep='\t')
