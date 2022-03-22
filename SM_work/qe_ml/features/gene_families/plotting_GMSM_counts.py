# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 10:29:32 2019

@author: weixiong001

Plots scatterplots and correlation, between GM/SM gene count
and gene family size.
"""

import pandas as pd
from matplotlib import pyplot as plt

orthogrps_df = pd.read_csv('ath_ogrpGMSM_counts.txt',
                           sep='\t', index_col=0)

plt.scatter(orthogrps_df['SM_counts'], orthogrps_df['Total_genes'])
# Correlation below is 0.1632583324509195
orthogrps_df['SM_counts'].corr(orthogrps_df['Total_genes'])
plt.scatter(orthogrps_df['GM_counts'], orthogrps_df['Total_genes'])
# Correlation below is 0.28674458015718673
orthogrps_df['GM_counts'].corr(orthogrps_df['Total_genes'])
