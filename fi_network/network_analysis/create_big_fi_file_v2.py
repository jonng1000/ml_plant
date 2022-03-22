# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Create big feature importance file, in a matrix
Takes about 20min, corrects for 54 tti_cluster id features which should be
categorical instead of continuous

Modified from create_big_fi_file.py in 
D:/GoogleDrive/machine_learning/fi_network/before_correction/threshold04
"""

import os
import csv
import pandas as pd
from datetime import datetime

GO_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4'
DGE_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/dge_runs/output'
CATF_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/rest_catf_runs/output'
CONTF_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/output'
TTI_PATH = 'D:/GoogleDrive/machine_learning/ml_go_workflow/tti_runs/output'
MAP_DOC = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
OUTPUT = 'big_fi.txt'

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
dge_fi = get_fi_files(DGE_PATH)
catf_fi = get_fi_files(CATF_PATH)
contf_fi = get_fi_files(CONTF_PATH)
tti_fi = get_fi_files(TTI_PATH)

# GO fi
go_fi_df = []
for one in go_fi:
    file_path = GO_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_fi.txt')[0]
    name = name.replace('GO_', 'GO:')
    temp_df.columns = temp_df.columns.str.replace('rf', name)
    go_fi_df.append(temp_df)

# DGE fi    
dge_fi_df = []
for one in dge_fi:
    file_path = DGE_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_fi.txt')[0]
    temp_df.columns = temp_df.columns.str.replace('rf', name)
    dge_fi_df.append(temp_df)

# Other categorical features fi
catf_fi_df = []
for one in catf_fi:
    file_path = CATF_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_fi.txt')[0]
    temp_df.columns = temp_df.columns.str.replace('rf', name)
    catf_fi_df.append(temp_df)

# Mapping dictionary to convert my placeholder names for continuous features
# back to their original names
map_dict = {}
with open(MAP_DOC, newline='') as csvfile:
    creader = csv.reader(csvfile, delimiter='\t')
    for row in creader:
        map_dict[row[1]] = row[0]
# Continuous features
contf_fi_df = []
for one in contf_fi:
    file_path = CONTF_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    job_id = job_id = one.split('_fi.txt')[0]
    orig_name = map_dict[job_id]
    temp_df.columns = temp_df.columns.str.replace('rf', orig_name)
    contf_fi_df.append(temp_df)

# tti features fi
tti_fi_df = []
for one in tti_fi:
    file_path = TTI_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_fi.txt')[0]
    temp_df.columns = temp_df.columns.str.replace('rf', name)
    tti_fi_df.append(temp_df)

all_df = go_fi_df + dge_fi_df + catf_fi_df + contf_fi_df
big_df = pd.concat(all_df, axis=1)
# Correcting for tti_cluster_id features
tti_mapper = {x:x.replace('ttr', 'tti') for x in \
              big_df.index[big_df.index.str.startswith('ttr_cluster_id')]}
re_big_df = big_df.rename(index=tti_mapper)
re_big_df = re_big_df.drop(columns=re_big_df.columns\
                           [re_big_df.columns.str.startswith('ttr_cluster_id')])

combined = pd.concat([re_big_df] + tti_fi_df, axis=1)
combined.to_csv(OUTPUT, sep='\t')

'''
combined.shape
Out[12]: (11801, 9535)
'''
print('Script ended:', get_time())
