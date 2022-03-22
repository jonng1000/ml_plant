# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:58:17 2019

@author: weixiong001
"""

import json
import pandas as pd
import csv
import numpy as np

with open('../gene_families/ath_orthogroups.json', 'r') as fp:
    ath_orthgroups = json.load(fp)

single_copy = {}
for group in ath_orthgroups:
    if len(group) == 0:
        print('empty group??')
        break
    if len(ath_orthgroups[group]) != 1:
        for gene in ath_orthgroups[group]:
            if gene in single_copy:
                print('gene present!!')
                break
            else:
                single_copy[gene] = 0
    elif len(ath_orthgroups[group]) == 1:
        for gene in ath_orthgroups[group]:
            if gene in single_copy:
                print('gene present!!')
                break
            else:
                single_copy[gene] = 1        
        
sc_df = pd.DataFrame.from_dict(single_copy, 
                               orient='index', columns= ['single_copy'])

# These Arabidopsis GO terms have already been filtered to only include
# experimental evidence codes
# Copied from comparing_GMSM_tandem.py in D:\GoogleDrive\machine learning\
# data_sets_JN\features\tandem_duplicated
parent_folder = r'D:\GoogleDrive\machine learning\data_sets_JN\getting_targets'
with open(parent_folder + r'\GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        priGO = set(row)  # both set and list has same number of genes
with open(parent_folder + r'\GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        secGO = set(row)  # both set and list has same number of genes
        
sc_df['Category'] = np.nan
m1 = sc_df.index.isin(priGO)
m2 = sc_df.index.isin(secGO)
sc_df['Category'] = sc_df['Category'].mask(m1, 'GM')
sc_df['Category'] = sc_df['Category'].mask(m2, 'SM')
sc_df['Category'].fillna('no_label', inplace = True)

#sc_df['Category'].value_counts()
#Out[66]: 
#no_label    24178
#GM           1482
#SM            114
#Name: Category, dtype: int64

#Shows that there are no more nans
#sum(sc_df['Category'].value_counts()) == len(sc_df)
#Out[69]: True

sc_df.index.name = 'Genes'
sc_df.to_csv('singe_copy_GMSM.txt', sep='\t')
