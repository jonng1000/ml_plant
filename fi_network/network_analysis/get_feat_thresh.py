# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 14:35:56 2021

@author: weixiong001

Gets top 10 features, for each feature as class target. These targets have passed the 
F1/R sq threshold of >= 0.4
"""

import os
import pandas as pd
from datetime import datetime

FILE = 'big_fi.txt'
OUTPUT = 'features_pass_thresh.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


print('Script started:', get_time())

# Getting list of all targets which scored well
targets = []
for file in os.listdir('./'):
    if file.endswith('features.txt'):
        # Ignores outdated continuous features file
        if file == 'score04_contf_features.txt':
            continue
        df = pd.read_csv(file, sep='\t')
        targets.append(df)

all_targets = pd.concat(targets)
all_targets['class_label'] = all_targets['class_label'].str.replace('GO_', 'GO:')

big_df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# 9535 features used as targets, 11801 features with feature importance
# values
big_df.shape
Out[3]: (11801, 9535)
'''
selected = big_df.loc[:, all_targets['class_label']]
stacked = selected.transpose().stack()
g = stacked.groupby(level=0, group_keys=False)
top10 = g.nlargest(10)
reset = top10.reset_index()
reset['ranks'] = new_values = list(range(1,11)) * 1475
pivoted = reset.pivot(index='level_0', columns='ranks', values='features')
pivoted.columns.name = None
pivoted.index.name = 'features'
print('Script ended:', get_time())

pivoted.to_csv(OUTPUT, sep='\t')