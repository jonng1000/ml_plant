# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:22:41 2019

@author: weixiong001

This script counts the number of GM and SM genes, and total number
of genes, in each orthogroup.
"""

import pandas as pd
import numpy as np
import csv
import json

orthogrps_df = pd.read_csv('./OF_linux190919/Orthogroups.tsv',
                           sep='\t', index_col=0)

# Selecting Arabidopsis orthogroups, where each Orthogroup is an index,
#and the value in each othogroup is one string, containing all the genes
#in the group, hence further downstream processing is needed
ath = orthogrps_df['ath_modified']

ath_orthogrps = {}
for items in ath.iteritems(): 
    orthogroup = items[0]
    unprocessed_genes = items[1]
    # Deals with nan since not all orthogroups have genes for a specific
    # species
    if type(unprocessed_genes) == float:
        continue
    else:
        # Splits long string into a list of sublists, where each sublist is 
        # a gene with its long ID
        ug_split = unprocessed_genes.split(', ')
        # Splits each long gene ID and selects the ID which is a whole number,
        # as the gene's ID
        ug_split_split = [item.split('|')[1] for item in ug_split]
        # Converts the list of gene IDs (corrected) into a set for easy
        # membership testing
        ug_ss_set = set(ug_split_split)
        # Data checking
        if len(ug_ss_set) != len(ug_split_split):
            print('Error, duplicate genes')
            break
        # Data checking
        if orthogroup in ath_orthogrps:
            print('Error, group already present')
            break
        else:
            # Builds dict where each orthogroup is a key, and the value is
            # the set of all gene IDs in it
            ath_orthogrps[orthogroup] = ug_ss_set

# This section is to convert sets to list, so that json dump can be used
# to save Ath orthogroups
for_json = {}
for k in  ath_orthogrps:
    for_json[k] = list(ath_orthogrps[k])

with open('ath_orthogroups.json', 'w') as fp:
    json.dump(for_json, fp, sort_keys=True, indent=4)
            
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

ath_ogrp_counts = []
for k,v in ath_orthogrps.items():
    # Counts size of gene family, and number of GM and SM genes
    GM_count = 0
    SM_count = 0
    for gene in v:
        if gene in priGO:
            GM_count += 1
        if gene in secGO:
            SM_count += 1
    total_genes = len(v)
    
    if k in ath_ogrp_counts:
        print('Error, group already present')
        break
    else:
        ath_ogrp_counts.append([k, GM_count, SM_count, total_genes])
# Sorts according to gene family size        
ath_ogrp_counts.sort(key=lambda x: x[3], reverse = True)
# Writes all these gene family info into a tab-delimited file
with open('ath_ogrpGMSM_counts.txt', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['Orthogroup', 'GM_counts', 'SM_counts', 'Total_genes'])
    for row in ath_ogrp_counts:
        writer.writerow(row)
        


 
