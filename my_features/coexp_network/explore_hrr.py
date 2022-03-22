# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Explores HRR and draws histogram showing its distribution
"""

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

FILE = 'ARATH-matrix-HRR.txt'
FIG = 'hrr_hist.png'
RANK_TYPE = 'HRR'


df = pd.read_csv(FILE, sep='\t', header=None)
df.rename(columns={0: 'gene 1', 1: 'gene 2', 2: 'value', 3: 'HRR'}, inplace=True)

g = sns.histplot(data=df, x=RANK_TYPE, bins=16, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()
