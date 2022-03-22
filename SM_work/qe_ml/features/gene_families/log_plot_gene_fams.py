# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:22:41 2019

@author: weixiong001

From, gene_families.txt file, plots gene family size on log10 scale. Skips
SM since max family size is 40, so it doesnt make sense to log10 it.
"""

import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt
import seaborn as sns
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

ath_df = pd.read_csv('gene_families.txt', sep='\t', index_col=0)

##############################################################################
# This is to see gene family sizes in GM and SM genes
# Performing data analysis and plotting

GM = ath_df[ath_df['Category']=='GM']
SM = ath_df[ath_df['Category']=='SM']

ax = sns.distplot(GM['OG_size'], kde=False)
ax.set_xlabel('GM OG_size')
ax.set_yscale('log')
ax.minorticks_off()
# Doesn't work, buggy pic for both svg and pdf when opened in illustrator,
# used both to get corrected one
plt.savefig("GM_OG_log.svg")
plt.savefig("GM_OG_log.pdf", transparent=True)
plt.figure()
##############################################################################      

##############################################################################
# replacing na values with unlabelled, as nan values cannot be used for plotting
ath_df['Category'].fillna('unlabelled', inplace = True)
ul = ath_df[ath_df['Category']=='unlabelled']

ax = sns.distplot(ul['OG_size'], kde=False)
ax.set_xlabel('ul OG_size')
ax.set_yscale('log')
ax.minorticks_off()
plt.savefig("ul_OG_log.svg", transparent=True)
plt.savefig("ul_OG_log.pdf", transparent=True)
plt.figure()