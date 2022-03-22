# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:54:20 2019

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
import numpy as np
import csv
from matplotlib import pyplot as plt

# Original ratios from header of .csv file loaded here
GM_ratio = 0.2699055330634278
SM_ratio = 0.4298245614035088
nl_ratio = 0.5316816941020762

df = pd.read_csv('land_plants_ratios.csv', sep='\t', index_col=0, comment='#')

df['GM_ratio_divided'] = GM_ratio/df['GM_ratio']
df['SM_ratio_divided'] = SM_ratio/df['SM_ratio']
df['nl_ratio_divided'] = nl_ratio/df['nl_ratio']
df['GM_ratio_change_log2'] = df['GM_ratio_divided'].apply(np.log2)
df['SM_ratio_change_log2'] = df['SM_ratio_divided'].apply(np.log2)
df['nl_ratio_change_log2'] = df['nl_ratio_divided'].apply(np.log2)
                 
plt.bar(['GM_ratio', 'SM_ratio', 'nl_ratio'], [GM_ratio, SM_ratio, nl_ratio])
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_divided', 'SM_ratio_divided', 
                          'nl_ratio_divided']])
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_divided', 'SM_ratio_divided', 
                          'nl_ratio_divided']], showfliers=False)
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_change_log2', 'SM_ratio_change_log2', 
                          'nl_ratio_divided']])
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_change_log2','SM_ratio_change_log2', 
                          'nl_ratio_divided']], showfliers=False)

