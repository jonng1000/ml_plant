# -*- coding: utf-8 -*-
"""
Created on 140920

@author: weixiong
From dge_1HE.txt, prefixes dge_ at the start of each column
"""

import pandas as pd
import numpy as np

INPUT_FILE = 'dge_1HE.txt'
OUTPUT_FILE = 'dge_1HE_edited.txt'

df = pd.read_csv(INPUT_FILE, sep='\t', index_col=0)
'''
# ~26k genes and ~400 features (~200 conditions as each is split into up and
# down regulated, so features will be twice that)
>>> df.shape
(26440, 436)
'''

new_cols = {name: 'dge_' + name for name in df.columns}
df = df.rename(columns=new_cols)

df.to_csv(OUTPUT_FILE, sep='\t')

'''
# Checks to see if there's features with only 1 gene, there's none
threshold = len(df) - 1
# This is empty
to_drop = df.columns[(df == 0).sum() == threshold]

df
Out[19]: 
           dge_E-GEOD-61542_3_up  ...  dge_E-MTAB-6965_1_down
Gene                              ...                        
AT1G05010                    1.0  ...                     0.0
AT1G09970                    1.0  ...                     0.0
AT1G21130                    1.0  ...                     1.0
AT1G76680                    1.0  ...                     0.0
AT2G15390                    1.0  ...                     0.0
                         ...  ...                     ...
AT3G21825                    NaN  ...                     NaN
AT4G23120                    NaN  ...                     NaN
AT1G80133                    NaN  ...                     NaN
AT4G35710                    NaN  ...                     NaN
AT5G15853                    NaN  ...                     0.0

[26440 rows x 436 columns]
'''