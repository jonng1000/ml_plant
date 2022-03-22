# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:18:36 2020

@author: weixiong001

Seelect NUM best features from datatset and produces a smaller dataset
"""

import pandas as pd

NUM = 200
MI_FEAT = 'mi_golgi.txt'
FILE = 'Golgi_apparatus_GO.txt'
OUTPUT_FILE = 'Golgi_mi_GO.txt'
CLASS_LABEL = 'AraCyc annotation'

df = pd.read_csv(FILE, sep='\t', index_col=0)
mi_df = pd.read_csv(MI_FEAT, sep='\t', index_col=0)
top = mi_df[1:NUM+1]
selection = list(top.index)
selection.append(CLASS_LABEL)
smaller_df = df.loc[:, selection]
smaller_df.to_csv(OUTPUT_FILE, sep='\t')