# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:19:50 2020

@author: weixiong001

Selects x features randomly y times from file Z. 
Creates a new smaller dataset with x features during
each of the y times. Script should be run like this:
ran_feature_sel.py Z X Y
"""
import sys
import pandas as pd

CLASS_LABEL = 'AraCyc annotation'
# Input variables
file = sys.argv[1]  # ml data file
num_features  = int(sys.argv[2])  # ml data file
num_rounds  = int(sys.argv[3])  # ml data file
#print(sys.argv)

# Reading in data and dividing into classes
df = pd.read_csv(file, sep='\t', index_col=0)

# Code seciton here selects a random subset of the
# dataset
# Creates index with suba predictions
suba_feat = df.columns[df.columns.str.startswith('suba')]
# Creates new list with suba predictions and class features
suba_n_cl = list(suba_feat)
suba_n_cl.append(CLASS_LABEL)
# Actual number of random features, since suba predictions
# have to be inside
rem_features = num_features - len(suba_feat)
df_suba_cl_only = df.loc[:, suba_n_cl]
df_no_suba_cl = df.drop(suba_n_cl, axis=1)
for i in range(num_rounds):
    small_df = df_no_suba_cl.sample(rem_features, axis=1)
    ran_sel = pd.concat([df_suba_cl_only, small_df], axis=1)
    ran_sel.to_csv(file.split('_GO')[0] + str(i + 1)
                   + '_GO.txt', sep='\t')
