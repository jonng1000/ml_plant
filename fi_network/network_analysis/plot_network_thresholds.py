# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:45:06 2022

@author: weixiong001

Plot pic to see number of nodes and edges in the feature network with different
thresholds (top X% of mutual ranks)
"""
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'network_thresholds.txt'
FIG = 'network_thresholds.pdf'

df = pd.read_csv(FILE, sep='\t', index_col=0)
melted = pd.melt(df, id_vars=['threshold (%)'], value_vars=['nodes', 'edges'])

g = sns.lineplot(data=melted, x='threshold (%)', y='value', hue='variable', 
                 marker='o')
g.set_yscale('log')
g.set_xticks(df['threshold (%)'].values)
plt.tight_layout()
g.figure.savefig(FIG, transparent=True)
plt.close()
