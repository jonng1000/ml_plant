# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:08:51 2021

@author: weixiong001

Explore scores from ml workflow
"""

import os
import numpy as np
import pandas as pd

FILE = './ct_go_hp_linux.txt'
DATA_FOLDER = './output_ran100/'

data = pd.read_csv(FILE, sep='\t', header=None)
go_lst_set = set(data.loc[:,0])

df_lst = []
for one in os.listdir(DATA_FOLDER):
    if one.endswith('_scores.txt'):
        temp = one.split('_scores')[0]
        temp = temp.split('go_')[1]
        new = temp.replace('_', ':')
        df_lst.append(new)

ml_go_set = set(df_lst)
