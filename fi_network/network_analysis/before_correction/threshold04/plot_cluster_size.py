# -*- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong
From mcl clustering output calculates cluster size and plots histogram of cluster size
"""

import pandas as pd
import numpy as np
import csv
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'dump.data.mci.I20'
FIG = 'hist_cs.png'

with open(FILE, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    cluster_dict = {}
    cluster_id = 0
    for row in csv_reader:
        cluster_id += 1
        cluster_size = len(row)
        cluster_dict[cluster_id] = cluster_size

df = pd.DataFrame.from_dict(cluster_dict, orient='index')
df.index.name = 'cluster_id'
df = df.rename(columns={0: 'feat_cluster_size'})
'''
# 159 clusters
df.shape
Out[178]: (159, 1)

# Max and min cluster size
df['feat_cluster_size'].max()
Out[9]: 223

df['feat_cluster_size'].min()
Out[10]: 2

# Seeing where to put a cluster size threshold for cutoff
len(df.loc[df['feat_cluster_size'] <= 2, :])
Out[21]: 46

len(df.loc[df['feat_cluster_size'] <= 3, :])
Out[22]: 75

len(df.loc[df['feat_cluster_size'] <= 5, :])
Out[23]: 101

len(df.loc[df['feat_cluster_size'] <= 10, :])
Out[24]: 136
'''

g = sns.histplot(data=df, x='feat_cluster_size', bins=20, 
                 log_scale=(False, True))
g.set_xticks(np.arange(0, 220, 20))
g.figure.savefig(FIG)
plt.close()


