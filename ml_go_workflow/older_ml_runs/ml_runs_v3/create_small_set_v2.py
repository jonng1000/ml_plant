# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:34:46 2020

@author: weixiong001

Creates snmall ml dataset for quick tests
Modified from create_small_set_v2.py in
D:\GoogleDrive\machine_learning\my_features\ml_runs_v2
"""
import pandas as pd

ML_DATA = 'ml_dataset_dc.txt'
CLASS_LABEL = 'go_' + 'GO:0016020'
SMALL = 'small_test.txt' #  Small test
#SMALL = 'slightly_bigger2_test.txt'  # Bigger test

df = pd.read_csv(ML_DATA, sep='\t', index_col=0)

partial = df.sample(n=499, axis=1)
partial[CLASS_LABEL] = df[CLASS_LABEL]
full = partial.sample(n=500, axis=0)

# Just to try out
#full = df.sample(n=1000, axis=0)

full.to_csv(SMALL, sep='\t')
