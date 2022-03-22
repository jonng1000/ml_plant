# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 17:56:24 2021

@author: weixiong001

Create big score file, in a matrix
Modified from create_big_fi_file.py in D:\GoogleDrive\machine_learning\fi_network
hence some variable names are just copied from that, so may not make sense here
but code works
Takes about 1 min
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
OUTPUT = 'big_scores.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_scores_files(a_path):
    '''
    Gets a list of all scores files from the selected path
    '''
    list_fi = []
    for file in os.listdir(a_path):
        if file.endswith('_scores.txt'):
            list_fi.append(file)
    return list_fi


print('Script started:', get_time())

# Getting list of all scores files
go_fi = get_scores_files(GO_PATH)
dge_fi = get_scores_files(DGE_PATH)
catf_fi = get_scores_files(CATF_PATH)
contf_fi = get_scores_files(CONTF_PATH)


# GO scores
go_fi_df = []
for one in go_fi:
    file_path = GO_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_scores.txt')[0]
    name = name.replace('GO_', 'GO:')
    temp_df.rename(index={0:name},inplace=True)
    go_fi_df.append(temp_df)

# DGE scores    
dge_fi_df = []
for one in dge_fi:
    file_path = DGE_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_scores.txt')[0]
    temp_df.rename(index={0:name},inplace=True)
    dge_fi_df.append(temp_df)

# Other categorical features scores
catf_fi_df = []
for one in catf_fi:
    file_path = CATF_PATH + '/' + one
    temp_df = pd.read_csv(file_path, sep='\t', index_col=0)
    name = one.split('_scores.txt')[0]
    temp_df.rename(index={0:name},inplace=True)
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
    job_id = one.split('_scores.txt')[0]
    orig_name = map_dict[job_id]
    temp_df.rename(index={0:orig_name},inplace=True)
    contf_fi_df.append(temp_df)

all_df = go_fi_df + dge_fi_df + catf_fi_df + contf_fi_df
big_df = pd.concat(all_df)
big_df.to_csv(OUTPUT, sep='\t')

print('Script ended:', get_time())
