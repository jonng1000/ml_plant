# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Explores mutual ranks (MR) and draws histogram showing its distribution
"""

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

FILE = 'mutual_ranks.txt' 
FIG = 'fi_mr_hist_50bins.png'
OUTPUT = 'selected_ranks.txt'

# Cannot do the below due to some weird warnig
# FutureWarning: elementwise comparison failed; returning scalar instead,
# but in the future will perform
# elementwise comparison
# Something to do with a numpy and pandas clash, use the below workaround
#df = pd.read_csv(FILE, sep='\t', index_col=0)
df = pd.read_csv(FILE, sep='\t')
df.set_index(['id'], inplace=True)

g = sns.histplot(data=df, x='MR', bins=50, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()

sorted_df = df.sort_values(by=['MR'])

# Setting threshold
'''
# 1m edges
len(df)
Out[83]: 1 049 756

# Top 10% threshold
# Take 104 976
len(df)/10
Out[189]: 104975.6

'''

# Use this threshold as the number of egdes are reasonable
selected = sorted_df.iloc[:104976, :].copy()
selected['invert_ranks'] = selected['MR'].values[::-1]
selected.to_csv(OUTPUT, sep='\t')
