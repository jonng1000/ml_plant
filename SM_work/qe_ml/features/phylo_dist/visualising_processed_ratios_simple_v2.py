# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 19:00:22 2019

@author: weixiong001
"""
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('procesed_ratios_lca.txt', sep='\t', index_col=0, 
                 header=[0,1])

only_divided_ratios = df[[i for i in df.columns if 'divided' in i[1]]]
long_ratios = pd.melt(only_divided_ratios, value_vars=only_divided_ratios.columns.tolist())

plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=long_ratios,
                 hue_order=['eudicot_divided', 'angiosperm_divided',
                            'embryophyte_divided', 'viridiplantae_divided']
                 )
ax.set_ylabel('ratio_divided')
plt.savefig('ratios_w_outliers.svg')
plt.figure()

plt.figure(figsize=(20, 15))
ax = sns.boxplot(x="Category", y="value", hue="taxon", data=long_ratios,
                 hue_order=['eudicot_divided', 'angiosperm_divided',
                            'embryophyte_divided', 'viridiplantae_divided'],
                showfliers=False)
ax.set_ylabel('ratio_divided')
plt.savefig('ratios_no_outliers.svg')
plt.figure()

