# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Visualises distributions of oob F1 scores of all GO classes
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'combined_scores.txt'
FIG = 'boxplot_compare_scores.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# This section is for plotting
g = sns.boxplot(x='feature_type', y='oob_f1', data=df)
#g.set(xlabel='GO Classes')
g.figure.savefig(FIG)
plt.close()

