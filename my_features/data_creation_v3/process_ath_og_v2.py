# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in OrthoFinder results from Irene and creates a dataframe 
which contains genes and their corresponding orthogroup, gene family size 
(calculated based on genes from all species) and gene family size 
(calculated based on genes from arabidopsis only)

Finale output of the dataframe, saved to a file, has the above data,
except orthogroup ids, as thats not needed.

Modified from process_ath_og.py in
D:\GoogleDrive\machine_learning\my_features\data_creation_v2
"""

import pandas as pd
import csv

FILE = 'Orthogroups.txt'
OUTPUT = 'edited_Ath_og.txt'

# list containing all genes from all species
all_genes = []
# Dictionaries containing orthogroup size calculated from all species and
# arabidopsis only, and connects each arabidopsis gene to its orthogroup
ath_genes_og = {}
ath_og = {}
all_species_og = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Calculates orthogroup size for all species
        # Includes test to make sure orthogroup ids are unique
        og = row[0].split(':')[0]
        size = len(row) - 1
        if og in all_species_og:
            print('og', og, 'already present in dict')
        else:
            all_species_og[og] = size

        # Calculates orthogroup size for arabidopsis only
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        ath_size = len(ath_genes)
        ath_og[og] = ath_size
        # Creates list for containing all genes from all species
        all_genes.extend(genes)
        # Puts list of ath genes in a dictionary, according to orthogroup
        for a_gene in ath_genes:
            ath_genes_og[a_gene] = og
    # Check for unique genes after entire file is read, don't check during
    # each iteration in the for loop above as it is slow, takes more than a few
    # minutes
    # All genes are unique
    if len(set(all_genes)) != len(all_genes):
        print('duplicate genes here')

og_df = pd.DataFrame.from_dict(ath_genes_og, orient='index',
                               columns=['ort_orthogroup'])
og_df.index.name = 'Gene'
og_df['ort_ath_og_size'] = og_df['ort_orthogroup'].map(ath_og)
og_df['ort_all_og_size'] = og_df['ort_orthogroup'].map(all_species_og)
og_df2 = og_df.drop(columns=['ort_orthogroup'])
og_df2.to_csv(OUTPUT, sep='\t')

"""
>>> og_df.shape
(27655, 3)
>>> og_df.isnull().values.any()
False

og_df2
Out[98]: 
           ort_ath_og_size  ort_all_og_size
Gene                                       
AT1G03510              135             3075
AT1G03540              135             3075
AT1G04840              135             3075
AT1G05750              135             3075
AT1G06140              135             3075
                   ...              ...
AT1G10990                1                1
AT3G48180                1                1
AT3G48185                1                1
AT5G27247                1                1
AT1G55207                1                1

[27655 rows x 2 columns]
"""
