# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 01:18:50 2021

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'sorted_all_nodes_counts.txt'
FIG = 'all_edge_counts.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)

g = sns.histplot(data=df, x='diff_category', bins=20, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()
