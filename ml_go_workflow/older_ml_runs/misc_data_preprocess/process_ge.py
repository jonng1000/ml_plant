# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis gene expression from Irene
and does very simple preprocessing (data is already quite clean)
before saving it as a new file.
"""

import pandas as pd

FILE = 'data_preprocessing/Ath.spm'
OUTPUT = 'edited_Ath_v2.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.index.name = 'Gene'
prefix = FILE.split('.')[-1].upper()
df.rename(mapper=lambda x: prefix + '_' + x, axis='columns', inplace=True)

# Basic looking through the data
'''
# Number of cells in dataframe
>>> df.size
187184
# No missing values in dataframe
>>> df.isnull().values.any()
False
'''
df.to_csv(OUTPUT, sep='\t')
