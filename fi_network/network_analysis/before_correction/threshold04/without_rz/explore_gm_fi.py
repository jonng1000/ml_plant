# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Explores geometric mean of feature importance and 
draws histogram showing its distribution
"""

import seaborn as sns
from scipy import stats
from matplotlib import pyplot as plt
import pandas as pd

FILE = 'gmean_impt_fi.txt' 
FIG = 'fi_gm_hist.png'
FIG2 = 'fi_gm_norm_hist.png'


# Cannot do the below due to some weird warnig
# FutureWarning: elementwise comparison failed; returning scalar instead,
# but in the future will perform
# elementwise comparison
# Something to do with a numpy and pandas clash, use the below workaround
#df = pd.read_csv(FILE, sep='\t', index_col=0)
df = pd.read_csv(FILE, sep='\t')
df.set_index(['id'], inplace=True)

g = sns.histplot(data=df, x='MFI', bins=16, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()

df['MFI_stan'] = stats.zscore(df['MFI'])
g = sns.histplot(data=df, x='MFI_stan', bins=16, log_scale=(False, True))
g.figure.savefig(FIG2)
plt.close()
