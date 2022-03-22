# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Explores mutual ranks (MR) and draws histogram showing its distribution
"""

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

FILE = 'min_ranks.txt'
FIG = 'fi_minr_hist_50bins.png'
RANK_TYPE = 'MinR'

# Cannot do the below due to some weird warnig
# FutureWarning: elementwise comparison failed; returning scalar instead,
# but in the future will perform
# elementwise comparison
# Something to do with a numpy and pandas clash, use the below workaround
#df = pd.read_csv(FILE, sep='\t', index_col=0)
df = pd.read_csv(FILE, sep='\t')
df.set_index(['id'], inplace=True)

g = sns.histplot(data=df, x=RANK_TYPE, bins=50, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()

sorted_df = df.sort_values(by=[RANK_TYPE])