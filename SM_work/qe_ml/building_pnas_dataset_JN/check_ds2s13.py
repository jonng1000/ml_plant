# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 18:13:22 2019

@author: weixiong
"""

import os
import pandas as pd

file = 'd2s13.txt'
dataset = pd.read_csv(file, sep='\t', index_col=0)