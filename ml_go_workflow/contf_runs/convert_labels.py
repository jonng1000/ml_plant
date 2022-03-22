# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 19:06:14 2021

@author: weixiong001

Convert high scoring job ids, R sq >= 0.7, to their corresponding
continuous features names
Also uses other thresholds
"""
import csv
import pandas as pd

FILE = 'high_labels.txt'
FILE2 = 'labels_0_4.txt'
MAP_DOC = 'D:/GoogleDrive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
OUTPUT = 'high_contf_features.txt'
OUTPUT2 = 'score04_contf_features.txt'

# Mapping dictionary to convert my placeholder names for continuous features
# back to their original names
map_dict = {}
with open(MAP_DOC, newline='') as csvfile:
    creader = csv.reader(csvfile, delimiter='\t')
    for row in creader:
        map_dict[row[1]] = row[0]

# Replacing job_id with continuous features name
data = pd.read_csv(FILE, sep='\t', index_col=0)
new_data = data.replace({'class_label': map_dict})
new_data.to_csv(OUTPUT, sep='\t', index=False)

# Replacing job_id with continuous features name
data2 = pd.read_csv(FILE2, sep='\t', index_col=0)
new_data2 = data2.replace({'class_label': map_dict})
new_data2.to_csv(OUTPUT2, sep='\t', index=False)