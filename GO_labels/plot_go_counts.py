# -*- coding: utf-8 -*-
"""
Spyder Editor

Plot graph of counts of GO terms, vs all GO terms
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = './sort_GO_gene_counts.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

num_rows = len(data)
numbers_col = np.arange(1, num_rows+1)
data.insert(0, column='id', value=numbers_col)

picture = 'go_counts.png'
fig, ax = plt.subplots()
sns.lineplot(data=data, x='id', y='Counts', 
             ci=None)
#ax.set_yscale('log')  # used to make go_counts_ylog.png
plt.savefig(picture)
plt.close()