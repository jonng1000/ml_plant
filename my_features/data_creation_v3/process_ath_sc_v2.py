# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:58:17 2019

@author: weixiong001

Uses orthogroups from Irene's OrthoFinder results, to identify if
Arabidopsis genes are single copy or not 

Modified from process_ath_sc.py in
D:\GoogleDrive\machine_learning\my_features\data_creation_v2
"""

import pandas as pd
import csv

FILE = 'Orthogroups.txt'
OUTPUT = 'edited_Ath_sc.txt'

# Dictionaries containing orthogroups and their associated genes,
# from all species and arabidopsis only
# and connects each arabidopsis gene to its orthogroup
ath_genes_og = {}
ath_og = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Calculates orthogroup size for all species
        og = row[0].split(':')[0]
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        ath_og[og] = ath_genes
        for a_gene in ath_genes:
            ath_genes_og[a_gene] = og

single_copy = {}
for group in ath_og:
    # Some orthogroups have no arabidopsis genes in them
    # Checks to make sure genes in single_copy dict does not appear
    # twice
    if len(ath_og[group]) != 1:
        for gene in ath_og[group]:
            if gene in single_copy:
                print('gene present!!')
                break
            else:
                single_copy[gene] = 0
    elif len(ath_og[group]) == 1:
        for gene in ath_og[group]:
            if gene in single_copy:
                print('gene present!!')
                break
            else:
                single_copy[gene] = 1  

        
sc_df = pd.DataFrame.from_dict(single_copy, 
                               orient='index', 
                               columns= ['sin_single_copy'])

sc_df.index.name = 'Gene'
sc_df.to_csv('edited_Ath_sc.txt', sep='\t')

'''
sc_df
Out[117]: 
           sin_single_copy
Gene                      
AT1G03510                0
AT1G03540                0
AT1G04840                0
AT1G05750                0
AT1G06140                0
                   ...
AT1G10990                1
AT3G48180                1
AT3G48185                1
AT5G27247                1
AT1G55207                1

[27655 rows x 1 columns]

# Eyeball data with notepad+ to ensure that 1s occur in >1 gene
'''
