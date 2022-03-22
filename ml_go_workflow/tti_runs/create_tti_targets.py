# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Creates a list of the tti features as targets, to use for my ml workflow.
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
FT_FILE = '../feature_type.txt'
OUTPUT = 'class_labels_tti.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
# Reads in the file with the types of features
ft_df = pd.read_csv(FT_FILE, sep='\t', index_col=0)

tti_targets = data.columns[data.columns.str.startswith('tti_')]
# To get class name as a column
# Reassigned variable to make my downsteam codee work
temp = tti_targets
temp_df = temp.to_frame(index=False)
df = temp_df.rename({0: 'tti_labels'}, axis='columns')

df.to_csv(OUTPUT, sep='\t', columns=['tti_labels'], header=False, index=False)
