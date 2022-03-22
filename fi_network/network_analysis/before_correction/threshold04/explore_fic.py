# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Plots histogram of feature importance cluster sizes
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'fi_clusters.txt'
FIG = 'fi_clusters.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)

g = sns.histplot(data=df, x='feat_cluster_size')
g.set_xticks(np.arange(0, 250, 25))
g.figure.savefig(FIG)
plt.close()

