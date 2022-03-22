# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Selects only important features
Takes about 3 min
"""

import os
import csv
import pandas as pd
from datetime import datetime

FILE = 'big_fi.txt'
OUTPUT = 'impt_features_i.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


print('Script started:', get_time())

# Getting list of all targets which scored well
targets = []
for file in os.listdir('./'):
    if file.endswith('features.txt'):
        df = pd.read_csv(file, sep='\t')
        targets.append(df)

all_targets = pd.concat(targets)
all_targets['class_label'] = all_targets['class_label'].str.replace('GO_', 'GO:')

big_df = pd.read_csv(FILE, sep='\t', index_col=0)
selected = big_df.loc[all_targets['class_label'], all_targets['class_label']]

selected.to_csv(OUTPUT, sep='\t')

print('Script ended:', get_time())
