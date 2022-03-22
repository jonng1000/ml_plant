# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

Labels my ml dataset with class labels, based on GO_check_v2.py but skips
sanity checks of GO terms and genes, as that script already did it.
Hence this script has a new name.

Takes ~5 min to run
"""
import pandas as pd
import numpy as np

GO_SELECT = 'D:/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'
ML_DATA = 'ml_dataset.txt'
ML_DATA_LABEL = 'ml_data_label.txt'
# For selecting one class label
CLASS_LABEL = 'membrane'

colnames=['GO class', 'number', 'GO cat', 'GO name', 'genes'] 
selection = pd.read_csv(GO_SELECT, sep="\t", names=colnames, header=None)

data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
data['class_label'] = np.nan

# For selecting one class label
genes_series = selection.loc[selection['GO name'] == 'membrane', :]['genes']
genes_set = set(genes_series.str.split(' ').iloc[0])
data.loc[data.index.isin(genes_set), 'class_label'] = 1
data.loc[~data.index.isin(genes_set), 'class_label'] = 0
'''
# Checks to make sure the filling of my class_label column is done
# correctly
n [55]: data['class_label'].value_counts(dropna=True)
Out[55]: 
0.0    26773
1.0     3151
Name: class_label, dtype: int64

data['class_label'].value_counts(dropna=True).sum()
Out[56]: 29924
'''

data.to_csv(ML_DATA_LABEL, na_rep='NA', sep='\t')


