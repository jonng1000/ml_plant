# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 16:07:48 2021

@author: weixiong001

Testing how to unpack pickled models
"""

from joblib import dump, load

FILE = 'D:/GoogleDrive/machine_learning/ml_go_workflow/hp_test/all_results/output_71g1hp/go_GO_0000138_model'
FILE2 = 'D:/GoogleDrive/machine_learning/ml_go_workflow/hp_test/all_results/output_71g2hp/go_GO_0000138_model'

clf = load(FILE)
clf2 = load(FILE2) 