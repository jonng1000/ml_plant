# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:46:11 2020

@author: weixiong001

Test subprocess
"""


from goatools import obo_parser
from datetime import datetime
import pandas as pd
import pickle
import subprocess

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


df = pd.read_csv('small_test.txt', sep='\t', index_col=0)

result = subprocess.run(['python', 'test.py'], input=pickle.dumps(df), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
returned_df = pickle.loads(result.stdout)

