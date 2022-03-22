# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:31:25 2021

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'go_GO_0005829_scores_mod.txt'
FILE2 = 'go_GO_0016020_scores.txt'
OUTPUT = 'selected.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)
data.insert(0, 'GO_class', 'GO:0005829')
data2 = pd.read_csv(FILE2, sep='\t', index_col=0)
data2.insert(0, 'GO_class', 'GO:0016020')

combined = pd.concat([data, data2])

combined['time_start'] = pd.to_datetime(combined['time_start'], dayfirst=True)
combined['time_end'] = pd.to_datetime(combined['time_end'], dayfirst=True)
combined['time_taken'] = combined['time_end'] - combined['time_start']
combined['time_taken_(s)'] = combined['time_taken'].astype('timedelta64[s]')

selected = combined[['GO_class', 'model_name', 'time_taken_(s)']]
# Saving this to file, to show that there's not always error bars due to time
# being the same for some models
selected.to_csv(OUTPUT, sep='\t')

fig, ax = plt.subplots()
ax.set(yscale='log')
sns.barplot(data=selected, x='GO_class', y='time_taken_(s)', hue='model_name')
plt.savefig('go_class_time_pub.png')
plt.close()

fig, ax = plt.subplots()
ax.set(yscale='log')
sns.barplot(data=selected, x='model_name', y='time_taken_(s)')
plt.savefig('all_time_pub.png')
plt.close()