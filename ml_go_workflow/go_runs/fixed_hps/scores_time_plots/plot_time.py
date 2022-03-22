# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:56:13 2021

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'cores_time_taken.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

data.loc[:, 'time_start'] = pd.to_datetime(data['time_start'], dayfirst=True)
data.loc[:, 'time_end'] = pd.to_datetime(data['time_end'], dayfirst=True)
data['time_taken'] = data['time_end'] - data['time_start']
data['time_taken_(m)'] = data['time_taken'].astype('timedelta64[m]')
data = data.reset_index()

fig, ax = plt.subplots()
sns.barplot(data=data, x='cores', y='time_taken_(m)')
plt.savefig('cores_time.png')
plt.close()