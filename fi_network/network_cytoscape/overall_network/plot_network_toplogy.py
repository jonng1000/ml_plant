# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 15:20:48 2021

@author: weixiong001

Plot graphs to visualise network topology
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'coloured_orderedl_node_topology.csv'
FIG = 'betweeness_hist.pdf'
FIG2 = 'deg_dis_line.pdf'
FIG3 = 'clustering_coef_hist.pdf'

df = pd.read_csv(FILE, sep=',', index_col=0)
df = df.reset_index()
df = df.set_index('shared name')

selected = df.loc[:, ['BetweennessCentrality', 'ClusteringCoefficient', 'Degree']]

# Useful as there's limited degree values
deg_vc = selected['Degree'].value_counts()
deg_vc = deg_vc.reset_index()
deg_vc.rename(columns={'index': 'degree', 'Degree': 'frequency'}, inplace=True)
deg_vc.sort_values(by='degree', inplace=True)
deg_vc['freq_log10'] = np.log10(deg_vc['frequency'])
deg_vc['deg_log10'] = np.log10(deg_vc['degree'])

# Not useful as there's many decimale values
betc_v = selected['BetweennessCentrality'].value_counts()

g = sns.histplot(data=selected, x='BetweennessCentrality', bins=20, 
                 log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()

# Need to manually log both axis since seaborn only allows me to log x
g = sns.regplot(data=deg_vc, x='deg_log10', y='freq_log10')
g.figure.savefig(FIG2)
plt.close()

g = sns.histplot(data=selected, x='ClusteringCoefficient', bins=20)
g.figure.savefig(FIG3)
plt.close()

