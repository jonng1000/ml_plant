# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:42:22 2019

@author: weixiong001

Takes in Arabidopsis genes with GO terms and experimental evidence codes,
then group them according to GM/SM categories, and counts the number
of genes that have/have not been tandemly duplicated.

Does a permuation test and calculates p-value to see if proportion of tandemly
duplicated genes is higher than expected than chance

Variables ending with _0 indicate genes that are not tandemly duplicated and 
those ending with _1 are tandemly duplicated
"""

import pandas as pd
import numpy as np
import csv
import itertools

# These Arabidopsis GO terms have already been filtered to only include
# experimental evidence codes
parent_folder = r'D:\GoogleDrive\machine learning\getting_targets'
with open(parent_folder + r'\GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        priGO = row
with open(parent_folder + r'\GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        secGO = row
        
df = pd.read_csv('genes_tandem_dup.csv', sep='\t', index_col=0)
df['Category'] = np.nan
m1 = df.index.isin(priGO)
m2 = df.index.isin(secGO)
df['Category'] = df['Category'].mask(m1, 'GM')
df['Category'] = df['Category'].mask(m2, 'SM')

# GM and SM counts
#df['Category'].value_counts()
#Out[29]: 
#GM    1487
#SM     115
#Name: Category, dtype: int64

# NA oounts
#df.isna().sum()
#Out[26]: 
#tandem_dup        0
#Category      26053
#dtype: int64

df['Category'].fillna('no_label', inplace = True)
GMSM_tandem_counts = df.groupby('Category')['tandem_dup'].value_counts()

# Data in GMSM_tandem_counts 
#GMSM_tandem_counts
#Out[2]: 
#Category  tandem_dup
#GM        0             1435
#          1               52
#SM        0               92
#          1               23
#Name: tandem_dup, dtype: int64

GM_0, GM_1 = GMSM_tandem_counts[0], GMSM_tandem_counts[1]
SM_0, SM_1 = GMSM_tandem_counts[2], GMSM_tandem_counts[3]
nl_0, nl_1 = GMSM_tandem_counts[4], GMSM_tandem_counts[5]

#For use in permutation_test function below, loc corresponds to these values:
#loc = 0, GM_0
#loc = 1, GM_1
#loc = 2, SM_0
#loc = 3, SM_1
#loc = 4, nl_0
#loc = 5, nl_1

def permutation_test(dataframe, num, loc, td, no_td):
    '''
    Parameters
        dataframe: needs columns called tandem_dup and Category
        num: the number of times permutation is run
        loc: the location in the shuffled dataframe which corresponds to
        specific GM and SM values (tandem_dup) in dataframe. Needs to be 1,
        3, or 5
        td: number of tandemly duplicated genes
        no_td: number of genes not tandemly duplicated
    '''
    # test is the ratio of tandemly duplicated to not tandemly duplicated genes
    # in the original dataframe
    test = td/ (td + no_td)
    c = 0
    all_ratios = []
    for i in range(num):
        dataframe['tandem_dup'] = np.random.permutation(dataframe['tandem_dup'])
        # shuffled is the dataframe with tandem_dup shuffled
        shuffled = dataframe.groupby('Category')['tandem_dup'].value_counts()
        if (shuffled[loc] / (shuffled[loc-1] + shuffled[loc]) ) >= test:
            c += 1
        s_0, s_1 = shuffled[loc-1], shuffled[loc]
        ratio = s_1/ (s_0 + s_1)
        all_ratios.append(ratio)
    p_value = c / num
    avg = sum(all_ratios)/len(all_ratios)
    return p_value, avg, all_ratios


values_GM = permutation_test(df, 10000, 1, GM_1, GM_0)
values_SM = permutation_test(df, 10000, 3, SM_1, SM_0)
values_nl = permutation_test(df, 10000, 5, nl_1, nl_0)

print('Shuffled values')
print('GM p-value', values_GM[0], 'GM avg',  values_GM[1])
print('SM p-value', values_SM[0], 'SM avg',  values_SM[1])
print('no_labeled p-value', values_nl[0], 'no_labeled avg',  values_nl[1])
print('Original values')
print('GM_0', GM_0, 'GM_1', GM_1, 'GM ratio', GM_1 / (GM_1 + GM_0),
      'SM_0', SM_0, 'SM_1', SM_1, 'SM ratio', SM_1 / (SM_1 + SM_0),
      'nl_0', nl_0, 'nl_1', nl_1, 'no_labeled ratio', nl_1 / (nl_1 + nl_0) )

##############################################################################
# This block is when i compared the absolute number of tandemly duplicated
# genes between the categories
# Results using 1000 permutations, a few seconds to run
#print(pvalue_GM_0, pvalue_GM_1, pvalue_SM_0, pvalue_SM_1)
#0.0 1.0 1.0 0.0

# p-values only
# Results using 10 000 permutations, about 2 min to run
#print(pvalue_GM_0, pvalue_GM_1, pvalue_SM_0, pvalue_SM_1)
#0.0 1.0 1.0 0.0001
##############################################################################

##############################################################################
# This is when i calculated ratios, but my ratios is ratio of mean number of 0s
# and 1s (non-tandemly duplicated and tandemly duplicated respectively)
#GM p-value 1.0 GM avg_0 1353.8345 GM avg_1 133.1655 GM ratio_avg 0.09836172737509645
#SM p-value 0.0004 SM avg_0 104.7215 SM avg_1 10.2785 SM ratio_avg 0.09815080952812937
#Original values
#GM_0 1435 GM_1 52 GM ratio 0.03623693379790941 SM_0 92 SM_1 23 SM ratio 0.25
##############################################################################

# =============================================================================
# This is when i calculated ratios, but ratios are the avg of all ratios of 0s
# and 1s, each of these ratios is calculated per iteration
#Shuffled values
# GM p-value 1.0 GM avg 0.09839884648675669
# SM p-value 0.0 SM avg 0.0996010626960639
# Original values
# GM_0 1435 GM_1 52 GM ratio 0.03623693379790941 SM_0 92 SM_1 23 SM ratio 0.25
# nl_0 23653 nl_1 2400 no_labeled ratio 0.10146704434955396
# =============================================================================

combined = itertools.zip_longest(values_GM[2], values_SM[2], values_nl[2])
ratios_df = pd.DataFrame(combined, columns = ['GM_ratio', 'SM_ratio', 'nl_ratio'])

with open('p_values_ratios.csv', 'w', newline='') as csvfile:
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


