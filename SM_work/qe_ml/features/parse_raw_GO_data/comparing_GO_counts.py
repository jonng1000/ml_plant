# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:13:22 2019

@author: weixiong
"""

import pandas as pd

import csv

with open('all_children_GO0019748.csv', newline='') as csvfile1,\
    open('all_children_GO0044238.csv',  newline='') as csvfile2:
        reader1 = csv.reader(csvfile1, delimiter='\t')
        reader2 = csv.reader(csvfile2, delimiter='\t')
        for secondary_GOs in reader1:
            pass
        for primary_GOs in reader2:
            pass

goa_noiea = pd.read_csv('goa_noiea_filtered.csv', sep='\t')
others = pd.read_csv('all_species_GO_counts.csv', header=None,
                     names=['Gene', 'GO_class', 'Evidence', 'Organism'],
                     sep='\t')
combined = pd.concat([goa_noiea, others], axis=0, join='outer',
                   ignore_index=True)

# others.isna().any().any()  # False -> no nans
df_genes_pri = combined[combined['GO_class'].isin(primary_GOs)]
df_genes_sec = combined[combined['GO_class'].isin(secondary_GOs)]
pri_genes_count = df_genes_pri['Organism'].value_counts().rename("pri_GO") 
sec_genes_count = df_genes_sec['Organism'].value_counts().rename("sec_GO")
pri_sec_GOs = pd.concat([pri_genes_count, sec_genes_count], axis=1, sort=False)
pri_sec_GOs.sort_values('sec_GO', inplace=True, ascending=False)

# Output with the below code:
#
#pri_sec_GOs.head()
#Out[60]: 
#              pri_GO  sec_GO
#taxon:162425   387.0   263.0
#taxon:3702    3024.0   234.0
#taxon:746128    86.0   119.0
#taxon:7227    2118.0    88.0
#taxon:208964   292.0    50.0

# Tests
# Just to explore these datasets more, and see if all genes in the "noiea"
# set is in the "all" set
others_sec = others[others['GO_class'].isin(secondary_GOs)]
o_sec_genes_count = others_sec['Organism'].value_counts().rename("sec_GO")

noiea_sec = goa_noiea[goa_noiea['GO_class'].isin(secondary_GOs)]
noiea_sec_genes_count = noiea_sec['Organism'].value_counts().rename("sec_GO")
set_others = set(others['Gene'])
set_noiea = set(goa_noiea['Gene'])
set_noiea <= set_others

#Out[76]: True


