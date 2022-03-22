# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

Script is meant to take in Irene's orthogroups and orthogroups dnds file. but
not used coz it has too little genes
"""

import pandas as pd
import csv

FILE = 'Orthogroups.txt'
FILE2 = 'ortho2ratios.txt'
OUTPUT = 'ath_dnds_og.txt'


# Dictionary: connects each arabidopsis gene to its orthogroup
ath_og = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Includes test to make sure orthogroup ids are unique
        og = row[0].split(':')[0]
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        for gene in ath_genes:
            # Checking
            if gene in ath_og:
                print(gene, 'present')
            else:
                ath_og[gene] = og


dnds_ratios = pd.read_csv(FILE2, sep='\t', index_col=0)

ath_dnds = {}
og_no_values = set()
for ath_gene in ath_og:
    if ath_og[ath_gene] in dnds_ratios.index:
        value = dnds_ratios.loc[ath_og[ath_gene], 'dN/dS']
        ath_dnds[ath_gene] = value
    else:
        og_no_values.add(ath_og[ath_gene])
        
a_ogs = set(ath_og.values())
missing = a_ogs - set(dnds_ratios.index)
'''
# Shows that I have selected all arabidopsis genes
ath_letters = [x[:4] for x in ath_og.keys()]
set(ath_letters)
Out[10]: {'AT1G', 'AT2G', 'AT3G', 'AT4G', 'AT5G', 'ATCG', 'ATMG'}
# Checks to make sure, my arabidopsis genes are unique
len(ath_og.keys())
Out[63]: 27655
len(set(ath_og.keys()))
Out[64]: 27655
'''
