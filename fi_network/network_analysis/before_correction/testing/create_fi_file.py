# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Create feature importance file, in a matrix
"""

import os
import csv
import pandas as pd
from datetime import datetime

GO_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4'
OUTPUT = 'GO_fi.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_fi_files(a_path):
    '''
    Gets a list of all feature importance files from the selected path
    '''
    list_fi = []
    for file in os.listdir(a_path):
        if file.endswith('_fi.txt'):
            list_fi.append(file)
    return list_fi


print('Script started:', get_time())

# Getting list of all feature importance files
go_fi = get_fi_files(GO_PATH)

# GO fi
go_fi_df = []
for one in go_fi:
    file_path = GO_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_fi.txt')[0]
    name = name.replace('GO_', 'GO:')
    temp_df.columns = temp_df.columns.str.replace('rf', name)
    go_fi_df.append(temp_df)

all_df = go_fi_df   # dummy variable, leftover from a previous script
big_df = pd.concat(all_df, axis=1)
big_df.to_csv(OUTPUT, sep='\t')

print('Script ended:', get_time())
