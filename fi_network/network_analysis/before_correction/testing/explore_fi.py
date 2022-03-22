# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:28:29 2021

@author: weixiong001

Takes about a few minutues
Plots histogram of feature importance values
"""

from datetime import datetime
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'GO_fi.txt'
FIG = 'GO_fi.png'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

df = pd.read_csv(FILE, sep='\t', index_col=0)
stacked = df.stack()
all_values = stacked.reset_index()
all_values.rename(columns={0: 'fi'}, inplace=True)

g = sns.histplot(data=all_values, x='fi', bins=16, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()
