# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 12:22:22 2019

@author: weixiong001

Shuffles genes and calculates proportion of genes which are single copy vs
non-single copy. Writes this dataframe to a .csv file. Script takes 4min to run
with 10 000 shuffles per gene category 
"""

import pandas as pd
import numpy as np
import csv
import itertools

df = pd.read_csv('singe_copy_GMSM.txt', sep='\t', index_col=0)
GMSM_sc = df.groupby('Category')['single_copy'].value_counts()

GM_0, GM_1 = GMSM_sc[0], GMSM_sc[1]
SM_0, SM_1 = GMSM_sc[2], GMSM_sc[3]
nl_0, nl_1 = GMSM_sc[4], GMSM_sc[5]

ratios = []
for label, x,y in [('GM_ratio', GM_0, GM_1), 
                   ('SM_ratio', SM_0, SM_1), ('nl_ratio', nl_0, nl_1)]:
    orig_ratio = y / (x + y)
    ratios.append(orig_ratio)
    print(label, orig_ratio)

def permutation_test(dataframe, num, id_cat, p, no_p, p_string):
    '''
    Parameters
        dataframe: needs 2 columns, one with the parameter of interest, and 
        GM/SM/nl category
        num: the number of times permutation is run
        loc: the location in the shuffled dataframe which corresponds to
        specific GM and SM values in dataframe. Needs to be 1,
        3, or 5
        p: parameter, number of genes with value of 1 (parameter is true)
        no_p: number of genes with value of 0 (parameter is false)
        p_string: parameter's name as a string
        id_cat: GM/SM/no_label designation, refers to different categories of
        genes
    '''
    # test is the ratio of parameter (when true) to parameter (when false)
    # in the original dataframe
    
    test = p / (no_p + p)
    c = 0
    all_ratios = []
    for i in range(num):
        dataframe[p_string] = np.random.permutation(dataframe[p_string])
        # shuffled is the dataframe with tandem_dup shuffled
        shuffled = dataframe.groupby('Category')[p_string].value_counts()
        if (shuffled[id_cat][1] / 
            (shuffled[id_cat][0] + shuffled[id_cat][1])
            ) >= test:
            c += 1
        s_0, s_1 = shuffled[id_cat][0], shuffled[id_cat][1]
        ratio = s_1 / (s_0 + s_1)
        all_ratios.append(ratio)
    p_value = c / num
    avg = sum(all_ratios)/len(all_ratios)
    return p_value, avg, all_ratios

values_GM = permutation_test(df, 10000, 'GM', GM_1, GM_0, 'single_copy')
values_SM = permutation_test(df, 10000, 'SM', SM_1, SM_0, 'single_copy')
values_nl = permutation_test(df, 10000, 'no_label', nl_1, nl_0, 'single_copy')

print('Shuffled values')
print('GM p-value', values_GM[0], 'GM avg',  values_GM[1])
print('SM p-value', values_SM[0], 'SM avg',  values_SM[1])
print('no_labeled p-value', values_nl[0], 'no_labeled avg',  values_nl[1])
print('Original values')
print('GM_0', GM_0, 'GM_1', GM_1, 'GM ratio', GM_1 / (GM_1 + GM_0),
      'SM_0', SM_0, 'SM_1', SM_1, 'SM ratio', SM_1/ (SM_1 + SM_0),
      'nl_0', nl_0, 'nl_1', nl_1, 'no_labeled ratio', nl_1/ (nl_1 + nl_0) ) 

combined = itertools.zip_longest(values_GM[2], values_SM[2], values_nl[2])
ratios_df = pd.DataFrame(combined, columns = ['GM_ratio', 'SM_ratio', 'nl_ratio'])

with open('single_copy_ratios.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['#Shuffled values'])
    writer.writerow(['#GM p-value', values_GM[0]])
    writer.writerow(['#GM avg', values_GM[1]])
    writer.writerow(['#SM p-value', values_SM[0]])
    writer.writerow(['#SM avg',  values_SM[1]])
    writer.writerow(['#nl p-value', values_nl[0]])
    writer.writerow(['#nl avg',  values_nl[1]])
    writer.writerow(['#Original values'])
    writer.writerow(['#GM_0', GM_0])
    writer.writerow(['#GM_1', GM_1])
    writer.writerow(['#GM ratio', GM_1 / (GM_1 + GM_0) ])
    writer.writerow(['#SM_0', SM_0,])
    writer.writerow(['#SM_1', SM_1])
    writer.writerow(['#SM ratio', SM_1 / (SM_1 + SM_0) ])
    writer.writerow(['#nl_0', nl_0,])
    writer.writerow(['#nl_1', nl_1])
    writer.writerow(['#nl ratio', nl_1 / (nl_1 + nl_0) ])
    ratios_df.to_csv(csvfile, sep='\t')

