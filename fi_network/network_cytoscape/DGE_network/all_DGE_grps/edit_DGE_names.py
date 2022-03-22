# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 17:50:05 2021

@author: weixiong001

Modify DGE expt names by indicating whether it has up or down regulated genes
"""

import pandas as pd

FILE = 'DGE_category_specific_expt.txt'
OUTPUT = 'DGE_names_status.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

df['up_down'] = df['Experiment'].str.split('_').str[-1]
'''
set(df['Experiment'].str.split('_').str[-1])
Out[9]: {'down', 'up'}
'''
df['expt_name'] = df['Specific_name'] + '_' + df['up_down']

df.to_csv(OUTPUT, sep='\t')