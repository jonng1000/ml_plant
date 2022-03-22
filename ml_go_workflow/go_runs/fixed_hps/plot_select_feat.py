# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 22:01:44 2022

@author: weixiong001
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = './output4/go_GO_1903508_fi.txt'
FILE2 = './output4/go_GO_1903508_scores.txt'
FIG = 'GO_1903508_fi.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

selected_fi = df.iloc[:10].copy()
selected_fi.rename(columns={'rf': "feature importance"}, inplace=True)
df_plot = selected_fi.reset_index()

plt.figure()
g = sns.barplot(x='features', y='feature importance', data=df_plot)
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
plt.savefig(FIG, transparent=True)
plt.close()