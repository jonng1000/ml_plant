# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:24:54 2020

@author: weixiong001

Plotting graph to see how my results look like
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'dge_1HE_edited.txt'
'''
# 264440 genes and 436 features (218 conditions, each with up and down
regulated status as feature)
df.shape
Out[95]: (26440, 436)
'''
df = pd.read_csv(FILE, sep="\t", index_col=0)

up_array = df.columns[df.columns.str.contains('up')]
down_array = df.columns[df.columns.str.contains('down')]
up_df = df.loc[:, up_array]
down_df = df.loc[:, down_array]

up_long = pd.melt(up_df)
up_long_1 = up_long.loc[up_long['value'] == 1, :]
down_long = pd.melt(down_df)
down_long_1 = down_long.loc[down_long['value'] == 1, :]

fig, ax = plt.subplots(figsize=(20, 15))
ax = sns.countplot(x='variable', data=up_long_1,
                   order=up_long_1['variable'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.savefig('up_regulated_genes.png')
plt.clf()

fig, ax = plt.subplots(figsize=(20, 15))
ax = sns.countplot(x='variable', data=down_long_1,
                   order=down_long_1['variable'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.savefig('down_regulated_genes.png')
plt.clf()

'''
# To check
up_long_1['variable'].value_counts()
Out[66]: 
E-GEOD-81361_up       7817
E-GEOD-77017_2_up     7104
E-GEOD-60835_1a_up    6906
E-GEOD-60835_1b_up    6540
E-GEOD-61542_3_up     6239

E-GEOD-79885_3_up        1
E-MTAB-3279_3_up         1
E-GEOD-79885_1a_up       1
E-GEOD-79856_up          1
E-MTAB-3279_2_up         1
Name: variable, Length: 206, dtype: int64

down_long_1['variable'].value_counts()
Out[67]: 
E-GEOD-81361_down       7444
E-GEOD-77017_2_down     6968
E-GEOD-60835_1b_down    6579
E-GEOD-60835_1a_down    6373
E-GEOD-72806_1c_down    6030

E-MTAB-3279_1_down         1
E-GEOD-38464_1b_down       1
E-MTAB-4380_down           1
E-GEOD-54677_down          1
E-MTAB-3279_3_down         1
Name: variable, Length: 208, dtype: int64
'''

