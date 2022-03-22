# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 23:12:53 2021

@author: weixiong001

Create test DGE dataset for ml DGE workflow
"""

import pandas as pd

FILE = 'ml_dataset_dc.txt'
OUTPUT = 'test_dataset_dge.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
small = data.iloc[:100, :100]
# This is just to use these two DGE labels as my test labels
dge_labels = ['dge_E-GEOD-61542_3_up', 'dge_E-GEOD-61542_3_down',
              'dge_E-GEOD-39217_1c_up', 'dge_E-GEOD-39217_1c_down']
limited = data.loc[:, dge_labels][:100]
small_test = pd.concat([small, limited], axis=1)

small_test.to_csv(OUTPUT, sep='\t')
