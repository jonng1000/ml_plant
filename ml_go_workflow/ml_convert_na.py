# -*- coding: utf-8 -*-
"""
Created on Wed 24 Aug 2022

@author: weixiong001

Insert NAs in the raw ml data to make the editor happy
"""
import pandas as pd
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


print('Script started:', get_time())
ML_DATA = 'ml_dataset.txt'
OUTPUT = 'ml_dataset_na.txt'

data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
data.to_csv(OUTPUT, sep='\t', na_rep='NA')

print('Script ended:', get_time())
