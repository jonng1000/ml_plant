# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in gene expression information and protein domain information
and combines it into a new file for machine learning. This is semi-raw data
as protein domains have been processed into binary features, but gene expression
information has not been sacled
"""

import pandas as pd

GE_FILE = 'edited_Ath.txt'
PD_FILE = 'protein_doms.txt'
OUTPUT = 'combined_data.txt'

ge_df = pd.read_csv(GE_FILE, sep='\t', index_col=0)
pd_df = pd.read_csv(PD_FILE, sep='\t', index_col=0)

com_df = pd.concat([ge_df, pd_df], axis=1)
com_df.index.name = 'Gene'
only_PD = com_df[com_df.columns[pd.Series(com_df.columns).str.startswith('PD_')]]
only_GE = com_df[com_df.columns[pd.Series(com_df.columns).str.startswith('GE_')]]
# Basic looking through the data
'''
# Number of cells in dataframe
>>> com_df.size
259149702
# Dataframe dimensions
>>> com_df.shape
(26733, 9694)
# Number of missing values in dataframe
>>> com_df.isnull().values.sum()
10623164
# % of missing values in dataframe
>>> (com_df.isnull().values.sum()/com_df.size) * 100
4.099238362234351
# Distribution of missing values in protein domain and gene expression dataframes
>>> only_PD.isnull().values.sum()
10596484
>>> only_GE.isnull().values.sum()
26680
'''
# Using .loc followed by inplace fillna doesn't work, hence need to write the
# below lines of code instead of doing this in one step
# Using inplace=True raises SettingWithCopyWarning, hence used this
only_PD = only_PD.fillna(0)
com_df = pd.concat([only_GE, only_PD], axis=1)
'''
# Shows that NA values are due to gene expression
>>> only_PD.isnull().values.sum()
0
>>> com_df.isnull().values.sum()
26680
'''
com_df.to_csv(OUTPUT, sep='\t')
