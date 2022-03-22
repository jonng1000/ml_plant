# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:29:26 2020

@author: weixiong001

Randomly shuffles feature values for ml data
"""

import os
import pandas as pd

DATA_FOLDER = 'D:/GoogleDrive/machine_learning/my_features/ml_runs_v2/labels_16_data'

# Seed number for randomisation
NUM = 1

for a_file in os.listdir(DATA_FOLDER):
    # This code block involves iterating and reading in files
    file_path = DATA_FOLDER + '/' + a_file
    # cell location name
    cell_loc = a_file.split('_', 1)[1].split('.')[0]
    # Reads in dataset, columns only
    data =  pd.read_csv(file_path, sep='\t', index_col=0)
    X = data.drop(columns=['class_label'])
    new_df = X.apply(lambda x: x.sample(frac=1, random_state=NUM).values)
    new_df['class_label'] = data['class_label']
    
    ran_file = a_file.split('.')[0] + '_ran.txt'
    new_df.to_csv(ran_file, sep='\t')
