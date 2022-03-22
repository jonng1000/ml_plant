# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:47:33 2019

@author: weixiong001

This script calculates original ratios over shuffled ratios of GM and SM, to
see which ratios has increased/decreased for each category 
"""

import pandas as pd
import seaborn as sns
import numpy as np
import csv
from matplotlib import pyplot as plt

with open('p_values_ratios.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    desired_rows = []
    for row in reader:
        if row[0].startswith('#'):
            desired_rows.append(row)
        else:
            break

df = pd.read_csv('p_values_ratios.csv', sep='\t', index_col=0, comment='#')
# orignal ratios, calculated from comparing_GMSM_tandem.py
GM_ratio = 0.0349697377269670
SM_ratio = 0.2
no_labeled_ratio = 0.0921199094154224
df['GM_ratio_divided'] = GM_ratio/df['GM_ratio']
df['SM_ratio_divided'] = SM_ratio/df['SM_ratio']
df['nl_ratio_divided'] = no_labeled_ratio/df['nl_ratio']
df['GM_ratio_change_log2'] = df['GM_ratio_divided'].apply(np.log2)
df['SM_ratio_change_log2'] = df['SM_ratio_divided'].apply(np.log2)
df['nl_ratio_change_log2'] = df['nl_ratio_divided'].apply(np.log2)

plt.figure()
ax = sns.violinplot(data=df[['nl_ratio_change_log2', 'GM_ratio_change_log2', 
                             'SM_ratio_change_log2']])
plt.figure()
ax = sns.violinplot(data=df[['GM_ratio_change_log2', 
                             'SM_ratio_change_log2']])
plt.figure()
ax = sns.boxplot(data=df[['nl_ratio_change_log2', 'GM_ratio_change_log2', 
                          'SM_ratio_change_log2']])
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_change_log2',
                          'SM_ratio_change_log2']])
plt.figure()
ax = sns.boxplot(data=df[['nl_ratio_change_log2', 'GM_ratio_change_log2', 
                          'SM_ratio_change_log2']], showfliers=False)
plt.figure()
ax = sns.boxplot(data=df[['GM_ratio_change_log2',
                          'SM_ratio_change_log2']], showfliers=False)
plt.figure()
ax = sns.boxplot(data=df[['nl_ratio_divided', 'GM_ratio_divided', 
                          'SM_ratio_divided']])
plt.savefig("td_ratiosd_out.svg")    
    
plt.figure()
ax = sns.boxplot(data=df[['nl_ratio_divided', 'GM_ratio_divided', 
                          'SM_ratio_divided']], showfliers=False)  
plt.savefig("td_ratiosd.svg")

df[['GM_ratio_change_log2', 'SM_ratio_change_log2', 'nl_ratio_change_log2']].describe()

plt.figure()
plt.bar(['nl', 'GM', 'SM_rati-+o'], 
        [no_labeled_ratio, GM_ratio, SM_ratio])
plt.ylabel('proportion of tandem duplicated genes')
plt.savefig("prop_td.svg")

