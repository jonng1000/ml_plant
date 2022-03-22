# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:43:18 2021

@author: weixiong001
"""

import pandas as pd

FILE= 'processed_results.txt'
OUTPUT = 'ath_pi_mw.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
selected = df.loc[:, ['mw', ' IPC_protein']]
renamed = selected.rename(columns={'mw': 'pep_mw', ' IPC_protein': 'pep_IPC_protein'})
renamed.to_csv(OUTPUT, sep='\t')

'''
renamed
Out[194]: 
             pep_mw  pep_IPC_protein
Gene                                
ATCG00500  55609.88            5.677
ATCG00510   4134.05            9.370
ATCG00280  51867.80            6.402
ATCG00890  42478.07            6.198
ATCG01250  42478.07            6.198
            ...              ...
AT5G39100  23979.46            5.347
AT5G58460  95833.29            7.322
AT5G46874   9238.77            6.854
AT5G47240  44778.26            5.944
AT5G52115  14810.70            7.439

[27654 rows x 2 columns]
'''