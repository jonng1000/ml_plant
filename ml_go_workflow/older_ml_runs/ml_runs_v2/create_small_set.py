# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:34:46 2020

@author: weixiong001

Creates snmall ml dataset for quick tests
"""

import pandas as pd

ML_DATA = './labels_16_data/ml_Golgi_apparatus.txt'
SMALL = 'small_test.txt'

df = pd.read_csv(ML_DATA, sep='\t', index_col=0)

partial = df.sample(n=500, axis=0)
y = partial.loc[:, 'class_label']

full = partial.sample(n=499, axis=1)
full['class_label'] = y

full.to_csv(SMALL, na_rep='NA', sep='\t')
