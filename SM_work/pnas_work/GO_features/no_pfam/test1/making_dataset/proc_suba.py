# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Edited from fully_proc_suba.py
Takes processed output from preprocessing.py and adds in suba
predictions as features
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

FILE = 'preprocessed_data.txt'
SUBA = 'Suba4-2020-3-12_17-2.csv'

data_f = pd.read_csv(FILE, sep='\t', index_col=0)
suba_df = pd.read_csv(SUBA, sep=',', index_col=0)
# Checked to make sure all genes are unique, they are
suba_df.rename(index=lambda s: s.split('.')[0], inplace=True)
suba_set = set(suba_df.index)

data_f_set = set(data_f.index)
# subs genes are a subset of my main df genes, but some of these genes are not
# in suba
# suba_set - data_f_set
# Out[71]: set()

# data_f_set - suba_set
# Out[156]: 
# {'AT1G45231',
#  'AT4G00520',
#  'AT4G03060',
#  'AT4G03060-CVI',
#  'AT4G32700',
#  'AT5G54130'}

data_f['suba'] = suba_df['location_consensus']
data_f.drop(list(data_f_set - suba_set), inplace=True)

# Created as a list,but will be converted to a set later
master_set = []
for x in set(suba_df['location_consensus']):
    temp_l = x.split(',')
    if len(temp_l) == 1:
        master_set.append(temp_l[0])
    else:
        master_set.extend(temp_l)
master_set = set(master_set)

# master_set
# Out[165]: 
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
    data_f['suba_' + pred] = data_f['suba'].str.contains(pred, regex=False).astype('int32')
data_f.drop(columns=['suba'], inplace=True)

# Predictions from suba are coded as int32 datatypes
# data_f.dtypes.astype(str).value_counts()
# Out[175]: 
# int64      4659
# float64      61
# int32        10
# dtype: int64

# This dataset has no nan except for class labels
data_f.to_csv('processed_suba.txt', sep='\t', na_rep='nan')


