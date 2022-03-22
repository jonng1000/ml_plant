# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:33:36 2021

@author: weixiong001

Plots hp tests results
Different from plot_hp_counts.py as this counts each set of parameters as one
group, instead of splitting up and counting each parameter individually.
Cuts off x-axis where logical to do so
"""


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from textwrap import wrap

FILE = './all_hp_counts_diff.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

#for score in ['high', 'med', 'low']:

def prep_df(data, score):
    '''
    Takes in a df (data), score (high, medium or low) and returns a
    df (df_plot), which is in the correct format for plotting. df_plot
    will only contain scores which match the score variable
    '''
    selected = data.loc[data['score'] == score, :]
    temp = selected.drop(columns=['score', 'count'])
    temp_score = selected.loc[:, 'score']
    temp_count = selected.loc[:, 'count']
    added = temp.astype(str).apply(lambda x : x.name + '_' + x)
    added_again = added.apply('_'.join, axis=1)
    added_again.name = 'param_set'
    
    df_plot = pd.concat([temp_score, added_again, temp_count], axis=1)
    df_plot['param_set'] = ['\n'.join(wrap(x, 60)) for x in  df_plot['param_set']]
    return df_plot


def plot_df(df_plot, score):
    '''
    Takes in a df for plotting (df_plot), score (high, medium or low) and 
    plots the df, showing counts of hp grps
    '''
    picture = score + '_count_trun.png'
    
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(data=df_plot, x='param_set', y='count', 
                 ci=None, marker= 'o', sort=False)
    ax.xaxis.set_tick_params(rotation=90, labelsize=7)
    plt.margins(x=0.01)
    plt.tight_layout()
    plt.savefig(picture)
    plt.close()
    return None


high_plot = prep_df(df, 'high')
med_plot = prep_df(df, 'med')
low_plot = prep_df(df, 'low')

hplot = high_plot.loc[high_plot['count'] >= 2, :]
mplot = med_plot.loc[med_plot['count'] >= 3, :]
lplot = low_plot.loc[low_plot['count'] >= 5, :]

plot_df(hplot, 'high')
plot_df(mplot, 'med')
plot_df(lplot, 'low')
