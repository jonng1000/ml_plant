# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Takes about a few minutues
Creates ranks from feature importance values of GO targets, 
removed feature importances of 0
"""

from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'GO_fi.txt'
FIG = 'nonzero_GO_fi_ranks.png'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

df = pd.read_csv(FILE, sep='\t', index_col=0)

stacked = df.stack()
all_values = stacked.reset_index()
'''
stacked.reset_index()
Out[15]: 
               features        level_1         0
0         go_GO:0022414  go_GO:0000003  0.039806
1         go_GO:0022414  go_GO:0000030  0.000000
2         go_GO:0022414  go_GO:0000038  0.000000
3         go_GO:0022414  go_GO:0000041  0.000000
4         go_GO:0022414  go_GO:0000096  0.000000
                ...            ...       ...
16257492  go_GO:0000003  go_GO:2000762  0.000000
16257493  go_GO:0000003  go_GO:2000904  0.000000
16257494  go_GO:0000003  go_GO:2001006  0.000000
16257495  go_GO:0000003  go_GO:2001020  0.000000
16257496  go_GO:0000003  go_GO:2001141  0.000000

[16257497 rows x 3 columns]

sum(all_values[0] == 0)
Out[18]: 15888792

# Vast majority are zero
15888792/16257497
Out[19]: 0.9773209246171166

all_values[0].value_counts()
Out[26]: 
0.000000    15888792
0.020000           6
0.000053           2
0.008891           2
0.000856           2
  
0.000139           1
0.003861           1
0.014406           1
0.010034           1
0.001544           1
Name: 0, Length: 368103, dtype: int64
'''

# Replaces 0 with nan to remove them
df.replace(0, np.nan, inplace=True)
ranks = df.rank(ascending=False)
stacked_r = ranks.stack()
all_ranks = stacked_r.reset_index()
all_ranks.rename(columns={0: 'ranks'}, inplace=True)

g = sns.histplot(data=all_ranks, x='ranks', bins=16, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()
