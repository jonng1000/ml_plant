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

FILE = 'ARATH.spm'
OUTPUT = 'edited_Ath_spm.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.index.name = 'Gene'
df.rename(mapper=lambda x: 'spm_' + x, axis='columns', inplace=True)

# Basic looking through the data
'''
# Number of cells in dataframe
>>> df.size
216396
# No missing values in dataframe
>>> df.isnull().values.any()
False
'''
df.to_csv(OUTPUT, sep='\t')

'''
df
Out[119]: 
           spm_Stem  spm_Female  ...  spm_Apical meristem  spm_Root meristem
Gene                             ...                                        
AT1G06620  0.046532    0.047420  ...             0.008240           0.620256
AT5G08160  0.102859    0.118691  ...             0.085536           0.087595
AT4G22890  0.310534    0.138270  ...             0.085655           0.039393
AT5G54067  0.000193    0.009688  ...             0.001262           0.000000
AT2G34630  0.084811    0.104203  ...             0.096461           0.145252
            ...         ...  ...                  ...                ...
AT3G58660  0.047040    0.114567  ...             0.169050           0.130233
AT3G50410  0.024343    0.016612  ...             0.055771           0.876591
AT5G64080  0.073535    0.302699  ...             0.153575           0.217980
AT1G09470  0.093172    0.153373  ...             0.323414           0.000000
AT1G76900  0.059785    0.079624  ...             0.057895           0.495803

[24044 rows x 9 columns]
'''
