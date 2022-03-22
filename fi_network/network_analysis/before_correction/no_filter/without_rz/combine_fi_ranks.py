# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Created combined file with all ranks
"""

import os
import pandas as pd


PATH = './output_ranks/'
OUTPUT = './all_ranks.text'

# Takes about 15min
df_lst = []
for file in os.listdir(PATH):
    file_path = PATH + file
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    df.drop(columns=['rf'], inplace=True)
    df_lst.append(df)

# Takes abt 6min
all_ranks = pd.concat(df_lst, axis=1)

# Saves all ranks
all_ranks.to_csv(OUTPUT, sep='\t')

