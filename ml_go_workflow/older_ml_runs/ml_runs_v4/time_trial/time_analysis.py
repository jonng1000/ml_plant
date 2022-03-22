# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:57:09 2021

@author: weixiong001

To analyse time taken for 3 tree models, on 16 cell locations
"""
import pandas as pd

FILE = 'time_cel_loc.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
data['time start'] = pd.to_datetime(data['time start'], dayfirst=True)
data['time end'] = pd.to_datetime(data['time end'], dayfirst=True)
data['time taken'] = data['time end'] - data['time start']
data['time taken (min)'] = data['time taken'].astype('timedelta64[m]')

"""
Find avg time
data.groupby(['model']).mean()
Out[42]: 
       time taken (min)
model                  
ada             58.6250
brf             46.8125
rf              79.6250
"""