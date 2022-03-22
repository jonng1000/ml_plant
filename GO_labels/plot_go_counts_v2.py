# -*- coding: utf-8 -*-
"""
Spyder Editor

Plot graph of counts of GO terms, vs all GO terms. Ensures Adobe Illustrator
can read fonts in pic.
Modified from plot_go_counts.py in 
D:\GoogleDrive\machine_learning\GO_labels
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = './sort_GO_gene_counts.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

num_rows = len(data)
numbers_col = np.arange(1, num_rows+1)
data.insert(0, column='id', value=numbers_col)

counts_vc = data['Counts'].value_counts()
counts_vc = counts_vc.reset_index()
counts_vc.rename(columns={'index': 'Gene size', 'Counts': 'Count'}, inplace=True)
counts_vc.sort_values(by='Gene size', inplace=True)
counts_vc['freq_log10'] = np.log10(counts_vc['Count'])
counts_vc['Gene size_log10'] = np.log10(counts_vc['Gene size'])

picture = 'go_counts_v2.pdf'
fig, ax = plt.subplots()
sns.histplot(data=data, x='Counts', bins=30)
ax.set_yscale('log')
plt.savefig(picture)
plt.close()

picture2 = 'go_counts_line_v2.pdf'
# Need to manually log both axis since seaborn only allows me to log x
g = sns.regplot(data=counts_vc, x='Gene size_log10', y='freq_log10')
g.figure.savefig(picture2)
plt.close()
