# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 23:12:53 2021

@author: weixiong001

Creates a test dataset for testing my ml workflow, puts in 2 GO classes to help
with it
"""

import pandas as pd

FILE = 'ml_dataset_dc.txt'
OUTPUT = 'test_dataset.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
small = data.iloc[:100, :100]
# This is just to use these two GO labels as my test labels
limited = data.loc[:, ['go_GO:0016020', 'go_GO:0005829']][:100]
small_test = pd.concat([small, limited], axis=1)

small_test.to_csv(OUTPUT, sep='\t')
