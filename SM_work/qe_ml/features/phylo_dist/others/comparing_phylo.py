# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:26:40 2019

@author: weixiong001

Does further data processing from output of find_lca.py.
- Creates a land_plants column which shows which gene belongs to any of the land plants taxa
- Classify genes according to GM/SM/no_label
- Did a permutation test to see how many genes in each category (GM/SM/no_label) belong to land
plants, and how many dont.
"""

import pandas as pd
import numpy as np
import csv
import itertools

df = pd.read_csv('genes_LCA.tsv', sep='\t', index_col=0)
land_plants_taxa = {'monocot', 'eudicot', 'angiosperm', 'bryophyte', 
                       'embryophyte'}

lca_each_gene = df.apply(lambda x: x.idxmax(), axis=1)
landplants_genes = lca_each_gene.isin(land_plants_taxa).astype(int)
df['land_plants'] = landplants_genes

#Total number of 1s and 0s equals total number of genes
#df['land_plants'].value_counts().sum()
#Out[47]: 25774


# These Arabidopsis GO terms have already been filtered to only include
# experimental evidence codes
parent_folder = r'D:/GoogleDrive/machine learning/getting_targets'
with open(parent_folder + r'/GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        priGO = row
with open(parent_folder + r'/GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        secGO = row
        
df['Category'] = np.nan
m1 = df.index.isin(priGO)
m2 = df.index.isin(secGO)
df['Category'] = df['Category'].mask(m1, 'GM')
df['Category'] = df['Category'].mask(m2, 'SM')
df['Category'].fillna('no_label', inplace = True)
df.to_csv('genes_landplants.txt', sep='\t')

lp_genes = df.groupby('Category')['land_plants'].value_counts()
GM_0, GM_1 = lp_genes[0], lp_genes[1]
SM_0, SM_1 = lp_genes[2], lp_genes[3]
# Be careful here, as order of numbers is switched from above, in future,
# can index but location instead
nl_1, nl_0 = lp_genes[4], lp_genes[5]

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
        if (shuffled[id_cat].loc[1] / 
            (shuffled[id_cat].loc[0] + shuffled[id_cat].loc[1])
            ) >= test:
            c += 1
        s_0, s_1 = shuffled[id_cat].loc[0], shuffled[id_cat].loc[1]
        ratio = s_1 / (s_0 + s_1)
        all_ratios.append(ratio)
    p_value = c / num
    avg = sum(all_ratios)/len(all_ratios)
    return p_value, avg, all_ratios

values_GM = permutation_test(df, 10000, 'GM', GM_1, GM_0, 'land_plants')
values_SM = permutation_test(df, 10000, 'SM', SM_1, SM_0, 'land_plants')
values_nl = permutation_test(df, 10000, 'no_label', nl_1, nl_0, 'land_plants')

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

with open('land_plants_ratios.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['#Shuffled values'])
    writer.writerow(['#GM p-value', values_GM[0]])
    writer.writerow(['#GM avg', values_GM[1]])
    writer.writerow(['#SM p-value', values_SM[0]])
    writer.writerow(['#SM avg',  values_SM[1]])
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