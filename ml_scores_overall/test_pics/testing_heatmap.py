# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:35:55 2021

@author: weixiong001

Generate heatmap of scores
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'go_scores.txt'
FILE2 = 'edited_catf_scores.txt'
FIG = 'test_heatmap.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 =  pd.read_csv(FILE2, sep='\t', index_col=0)

# Put another [] to ensure df is returned
# Not sure why breaking this line into separate lines prevents the heatmap
# from being plotted, but combining code into one line below seems to work
selected_go = df.loc[:, ['oob_f1']].transpose()
selected_go.sort_values(by='oob_f1', axis=1, inplace=True)
selected_go.rename(index={'oob_f1':'GO terms'},inplace=True)

selected = df2.loc[:, ['oob_f1']].transpose()
pid = selected.loc[:, selected.columns.str.startswith('pid_')]
# Doing it this way to prevent the warning about setting values on a view
pid = pid.sort_values(by='oob_f1', axis=1)
pid.rename(index={'oob_f1':'PPI cluster IDs'},inplace=True)
temp = pd.concat([selected_go, pid])
g_temp = sns.heatmap(temp, cmap='flare', xticklabels=False)
g_temp.set(xlabel='oob_F1')
g_temp.figure.savefig(FIG)
'''
# Just to test
# Seems to be ok, as two distinct heatmaps are shown, which allows me
# to clearly see how they are separate
temp = pd.concat([selected_go, selected])
g_temp = sns.heatmap(temp)
'''