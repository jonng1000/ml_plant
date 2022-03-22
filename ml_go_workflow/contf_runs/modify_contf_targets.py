# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Modifies list of continuous features as targets, adds in job id, to use for my
ml workflow.
"""

import pandas as pd

FILE = 'class_labels_contf.txt'
OUTPUT = 'mod_class_labels_contf.txt'

data = pd.read_csv(FILE, sep='\t', header=None)

job_lst = ['job_' + str(i) for i in range(len(data))]
data['job_id'] = job_lst

data.to_csv(OUTPUT, sep='\t', header=False, index=False)
