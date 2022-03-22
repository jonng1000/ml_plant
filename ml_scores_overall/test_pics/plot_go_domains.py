# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 19:05:57 2021

@author: weixiong001

Plot GO scores according to top level domains
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'go_scores_domains.txt'
FIG = 'go_dom_box.png'
FIG2 = 'go_dom_hist.png'
THRESH = 0.7

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Making plots
plt.figure()
g = sns.boxplot(data=df, x='GO_domain', y='oob_f1')
g.figure.savefig(FIG)
plt.close()

plt.figure()
g2 = sns.histplot(data=df, x='oob_f1', hue='GO_domain', 
                  element='step', log_scale=(False, True))
g2.figure.savefig(FIG2)
plt.close()

# Exploring data
everything = df['GO_domain'].value_counts()
'''
# Orignal numbers in each domain
df['GO_domain'].value_counts()
Out[419]: 
biological_process    994
molecular_function    234
cellular_component    151
Name: GO_domain, dtype: int64
'''
pass_thresh = df.loc[df['oob_f1'] >= THRESH, :]
pass_counts = pass_thresh['GO_domain'].value_counts()
'''
# High scoring numbers in each domain
pass_thresh['GO_domain'].value_counts()
Out[427]: 
biological_process    70
molecular_function    16
cellular_component    13
Name: GO_domain, dtype: int64

# Manually did the below division to verify that this is correct
# Doesnt seem to show any difference in proportion of high scoring groups
pass_counts/everything
Out[431]: 
biological_process    0.070423
molecular_function    0.068376
cellular_component    0.086093
Name: GO_domain, dtype: float64
'''
