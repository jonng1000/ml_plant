# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Creates a list of DGE class labels, to use for my ml workflow.
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
OUTPUT = 'class_labels_dge.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

dge_labels = df.columns[df.columns.str.startswith('dge_')]
# To get DGE class name as a column
temp = dge_labels.str.split('dge_').str[1]
temp_df = temp.to_frame(index=False)
df = temp_df.rename({0: 'dge_labels'}, axis='columns')

df.to_csv(OUTPUT, sep='\t', columns=['dge_labels'], header=False, index=False)
