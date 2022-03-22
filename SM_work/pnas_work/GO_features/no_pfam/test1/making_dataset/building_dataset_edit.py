# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:08:59 2019

@author: weixiong

Edited from building_dataset.py in 
D:\GoogleDrive\machine_learning\GMSM_ML\building_pnas_dataset_JN
This script takes individual .txt files (each a dataset) and combines them
to form one big dataframe - contains features for genes. Produces a data set
without pfam domains and aracy pathways.
"""

import os
import numpy as np
import pandas as pd

# =============================================================================
# Performs the operation to combines dataframe
empty_df = pd.DataFrame()
first = True
for file in os.listdir():
    if file.startswith('d2'):
        if first:
            dataset = pd.read_csv(file, sep='\t', index_col=0)
            print(file, 'loaded')
        else:
            dataset2 = pd.read_csv(file, sep='\t', index_col=0)
            dataset = dataset.join(dataset2, how='outer')
            print(file, 'joined')
        first = False

# Dimensons of dataframe after combining all features from pnas paper, without
# pfam domains. 5239 genes and 145 features
# dataset.shape
# Out[3]: (5239, 145)

dataset.index.name = 'Gene'

df_labels = pd.read_csv('d1s1.txt', sep='\t', index_col=0)
df_labels.drop(['AraCyc pathways'], axis=1, inplace=True)
dataset = dataset.join(df_labels, how='outer')

# dataset['AraCyc annotation'].value_counts(dropna=False)
# Out[14]: 
# none                                             2933
# Non-secondary metabolism pathway                 1306
# Secondary metabolism pathway                      423
# NaN                                               325
# Seconday and Non-secondary metabolism pathway     264
# Name: AraCyc annotation, dtype: int64

dataset = dataset.replace('none', np.nan)

# dataset['AraCyc annotation'].value_counts(dropna=False)
# Out[19]: 
# NaN                                              3258
# Non-secondary metabolism pathway                 1306
# Secondary metabolism pathway                      423
# Seconday and Non-secondary metabolism pathway     264
# Name: AraCyc annotation, dtype: int64

# After adding everything, without pfam domans and aracyc pathways
# the 146th feature is the class label
# dataset.shape
# Out[20]: (5251, 146)

dataset.to_csv("dataset_nopfam.txt", sep='\t', na_rep='NA')