# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Takes in ml results and produces plots to visualise time taken. Time trial with
10 random search iterations
"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'combined_scores_ttrs.txt'
FIG = 'time_ttrs.png'

# GO file
scores_df = pd.read_csv(FILE, sep='\t', index_col=0)

scores_df['time_start'] = pd.to_datetime(scores_df['time_start'], dayfirst=True)
scores_df['time_end'] = pd.to_datetime(scores_df['time_end'], dayfirst=True)
scores_df['time_taken'] = scores_df['time_end'] - scores_df['time_start']
scores_df['time_taken_(s)'] = scores_df['time_taken'].astype('timedelta64[s]')
scores_df['time_taken_(min)'] = scores_df['time_taken'].astype('timedelta64[m]')


# Long form for seaborn
melted = pd.melt(scores_df, id_vars=['class_label', 'model_name'],
                 value_vars=['time_taken', 'time_taken_(s)', 'time_taken_(min)'])
rem_melted = melted.drop_duplicates()
selected = rem_melted.loc[rem_melted['variable'] == 'time_taken_(min)', :]

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(data=selected, x='model_name', y='value')
ax.set_xlabel('model_name', fontsize=12)
ax.set_ylabel('time_taken_(min)', fontsize=12)
plt.tight_layout()
plt.savefig(FIG)
plt.close()
