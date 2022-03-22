# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

Takes the ml data with all 16 cell part labels by Marek, and separates it into
16 separate ml data files with 1 class label each.
"""
import pandas as pd

OUT_FOLDER = './labels_16_data'
ML_DATA = 'ml_16l_edited.txt'

# My ml data file
data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
cell_parts = data.columns[data.columns.str.startswith('class_label')]
for one in cell_parts:
    temp = list(cell_parts)
    temp.remove(one)
    smaller_df = data.drop(temp, axis=1)
    smaller_df.rename(columns={one: 'class_label'}, inplace=True)
    smaller_name = 'ml_' + one.split('_')[2] + '.txt'
    smaller_name = smaller_name.replace(' ', '_')
    location = OUT_FOLDER + '/' + smaller_name
    smaller_df.to_csv(location, na_rep='NA', sep='\t')


