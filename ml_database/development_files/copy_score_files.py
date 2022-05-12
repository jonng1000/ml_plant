# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 1725 2022

@author: weixiong001

Copies scores to a new folder, for creation of gzip folder for database upload.

Takes about 1h
"""

import shutil, os
import pandas as pd
from datetime import datetime

GO_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4'
DGE_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/dge_runs/output'
CONTF_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/contf_runs/output'
CONTF_MAP = 'G:/My Drive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
REST_CATF_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/rest_catf_runs/output'
TTI_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/tti_runs/output'
OUTPUT_FOLDER = 'C:/Users/weixiong001/Documents/other_database/all_scores_br/golabel'


def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_path(folder):
    """
    Get a list of all specified file paths in one folder, which contains
    trained models from a group of features
    """
    temp_files = [folder + '/' + one_file for one_file in os.listdir(folder)]
    all_files = [one_file for one_file in temp_files if one_file.endswith('_scores.txt')]
    return all_files


print('GO features start:', get_time())
file_paths = get_path(GO_FOLDER)
#file_paths = file_paths[:2] #  For checking
for f in file_paths:
    shutil.copy(f, OUTPUT_FOLDER)
print('end:', get_time())

print('DGE features start:', get_time())
file_paths = get_path(DGE_FOLDER)
# For testing
#file_paths = file_paths[:2]
for f in file_paths:
    shutil.copy(f, OUTPUT_FOLDER)
print('end:', get_time())

print('continuous features start:', get_time())
file_paths = get_path(CONTF_FOLDER)
#  For testing
#file_paths = file_paths[:2]
for f in file_paths:
    shutil.copy(f, OUTPUT_FOLDER)
print('end:', get_time())

print('rest of categorical features start:', get_time())
file_paths = get_path(REST_CATF_FOLDER)
#  For testing
#file_paths = file_paths[:2]
for f in file_paths:
    shutil.copy(f, OUTPUT_FOLDER)
print('end:', get_time())

print('tti features start:', get_time())
file_paths = get_path(TTI_FOLDER)
# For testing
#file_paths = file_paths[:2]
for f in file_paths:
    shutil.copy(f, OUTPUT_FOLDER)
print('end:', get_time())


