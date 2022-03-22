# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Create feature importance file with ranks, in a matrix
Takes about 20min
"""

import os
import csv
import pandas as pd
from datetime import datetime

GO_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4'
DGE_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/dge_runs/output'
CATF_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/rest_catf_runs/output'
CONTF_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/output'
MAP_DOC = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
OUTPUT = 'feature_ranks.txt'

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

def get_ranks(each, a_path):
    '''
    Converts feature importance for one df, into ranks
    '''
    file_path = a_path + '/' + each
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = each.split('_fi.txt')[0]
    df[name + '_fi_ranks'] = df['rf'].rank(ascending=False)
    df.drop(columns=['rf'], inplace=True)
    return df


print('Script started:', get_time())

# Getting list of all feature importance files
go_fi = get_fi_files(GO_PATH)
dge_fi = get_fi_files(DGE_PATH)
catf_fi = get_fi_files(CATF_PATH)
contf_fi = get_fi_files(CONTF_PATH)
# GO ranks
go_ranks = []
for one in go_fi:
    temp_df = get_ranks(one, GO_PATH)
    temp_df.columns = temp_df.columns.str.replace('GO_', 'GO:')
    go_ranks.append(temp_df)
# DGE ranks    
dge_ranks = []
for one in dge_fi:
    temp_df = get_ranks(one, DGE_PATH)
    dge_ranks.append(temp_df)
# Other categorical features ranks
catf_ranks = []
for one in catf_fi:
    temp_df = get_ranks(one, CATF_PATH)
    catf_ranks.append(temp_df)

# Mapping dictionary to convert my placeholder names for continuous features
# back to their original names
map_dict = {}
with open(MAP_DOC, newline='') as csvfile:
    creader = csv.reader(csvfile, delimiter='\t')
    for row in creader:
        map_dict[row[1]] = row[0]
# Continuous features ranks
contf_ranks = []
for one in contf_fi:
    temp_df = get_ranks(one, CONTF_PATH)
    job_id = temp_df.columns.str.split('_fi')[0][0]
    orig_name = map_dict[job_id]
    temp_df.columns = temp_df.columns.str.replace(job_id, orig_name)
    contf_ranks.append(temp_df)

all_df = go_ranks + dge_ranks + catf_ranks + contf_ranks
all_ranks = pd.concat(all_df, axis=1)
all_ranks.columns = all_ranks.columns.str.split('_fi_ranks').str[0]
all_ranks.to_csv(OUTPUT, sep='\t')

'''
all_ranks.max().max()
Out[9]: 10173.5

all_ranks.min().min()
Out[10]: 1.0

all_ranks.shape
Out[12]: (11801, 9535)
'''
print('Script ended:', get_time())
