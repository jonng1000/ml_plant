# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in OrthoFinder results from Irene, and determines if each
arabidopsis gene has paralogs. If there's >1 arabdiopsis gene in an orthogroup
(defined as only including arabidopsis genes), then those genes have paralogs.

But this is the inverse of my single copy, so not using it as my features
"""

import os
import pandas as pd
import csv

FILE = 'Orthogroups.txt'
OUTPUT = 'ath_paralogs.txt'


# Dictionary: connects each orthogroup to only arabidopsis gene
og_ath = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Includes test to make sure orthogroup ids are unique
        og = row[0].split(':')[0]
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        if og in og_ath:
            print(og, 'present')
        else:
            og_ath[og] = ath_genes

ath_paralogs = {}
for orthogroup in og_ath:
    if len(og_ath[orthogroup]) == 1:
        for gene in og_ath[orthogroup]:
            if gene in ath_paralogs:
                print(gene, 'present')
            else:
                ath_paralogs[gene] = 0
    elif len(og_ath[orthogroup]) > 1:
        for gene in og_ath[orthogroup]:
            if gene in ath_paralogs:
                print(gene, 'present')
            else:
                ath_paralogs[gene] = 1
        
para_df = pd.DataFrame.from_dict(ath_paralogs, 
                                 orient='index', 
                                 columns= ['par_paralogs'])

para_df.index.name = 'Gene'
para_df.to_csv('ath_paralogs.txt', sep='\t')


'''
# Shows that I have selected all arabidopsis genes

ath_letters = [x[:4] for x in ath_paralogs.keys()]
set(ath_letters)
Out[10]: {'AT1G', 'AT2G', 'AT3G', 'AT4G', 'AT5G', 'ATCG', 'ATMG'}
# Checks to make sure, my arabidopsis genes are unique
len(ath_paralogs.keys())
Out[63]: 27655
len(set(ath_paralogs.keys()))
Out[64]: 27655
'''

            
"""
# Dictionary: Shows what are the homologous species for each arabidopsis gene
ath_species = {}
for ath_gene in ath_og:
    orth = ath_og[ath_gene]
    homolog_species = og_species[orth]
    ath_species[ath_gene] = list(homolog_species)
    
ath_series = pd.Series(ath_species)
ath_df = ath_series.explode().to_frame()
expanded = pd.get_dummies(ath_df, prefix=['hom'])
expanded.index.name = 'Gene'

homologs_presence = expanded.groupby(['Gene']).sum()
'''
# Dimensions, includes arabidopsis, so need to remove as it doesn't makes sense
# as I am detecting homologs
homologs_presence.shape
Out[138]: (27655, 23)
'''
# Drop the arabidopsis column, as I only want homologs, hence this doesn't
# make sense
dropped = homologs_presence.drop(columns=['hom_Arabidopsis_thaliana'])
ath_homologs = dropped.loc[dropped.sum(axis=1)!=0, :]
ath_homologs.to_csv(OUTPUT, sep='\t')


ath_homologs.shape
Out[150]: (22920, 22)
"""
