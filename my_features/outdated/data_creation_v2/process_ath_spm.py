# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis gene expression from Irene
and does very simple preprocessing (data is already quite clean)
before saving it as a new file. Edited from process_ath_exp.py
in /mnt/d/GoogleDrive/machine_learning/my_features/data_preprocessing
"""

import pandas as pd

FILE = 'Ath.spm'
OUTPUT = 'edited_Ath_spm.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.index.name = 'Gene'
df.rename(mapper=lambda x: 'spm_' + x, axis='columns', inplace=True)

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
