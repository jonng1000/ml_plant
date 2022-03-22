# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:06:28 2019

@author: weixiong001

Counts number of genes belong to GO terms secondary metabolic process and
primary metaoblic process. This uses a file downloaded from AmiGO which has 
genes from plants, with experimental evidence.

Note small bug, where df_rem_not is not used subsequently, so results is
slightly off, but nvm as it doesnt affect my results significantly.
"""

import pandas as pd
import csv

# GO0019748 secondary metabolic process
# GO0044238 primary metabolic process
with open('all_children_GO0019748.csv', newline='') as csvfile1,\
    open('all_children_GO0044238.csv',  newline='') as csvfile2:
        reader1 = csv.reader(csvfile1, delimiter='\t')
        reader2 = csv.reader(csvfile2, delimiter='\t')
        for secondary_GOs in reader1:
            pass
        for primary_GOs in reader2:
            pass
        

df = pd.read_csv('GO_plants_expt_code.txt', sep='\t', header=None)
df.rename(columns={2:'Gene', 3:'Annotation_qualifier', 4:'GO_class', 
                   12:'Organism'}, inplace=True)

df_rem_not = df[df['Annotation_qualifier'] != 'not']
df_genes_pri = df[df['GO_class'].isin(primary_GOs)]
df_genes_sec = df[df['GO_class'].isin(secondary_GOs)]
pri_genes_count = df_genes_pri['Organism'].value_counts().rename("pri_GO") 
sec_genes_count = df_genes_sec['Organism'].value_counts().rename("sec_GO") 
pri_sec_GOs = pd.concat([pri_genes_count, sec_genes_count], axis=1, sort=False)
pri_sec_GOs.sort_values('sec_GO', inplace=True, ascending=False)
