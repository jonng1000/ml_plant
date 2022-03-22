# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:27:38 2019

@author: weixiong

Takes a .gff file, which is the genomic structure file and
creates a dict with has the location of all genes, sorted from start
to finish, according to increasing chromosome number. Determines
whether genes are tandemly duplicated by seeing if adjacent genes
are from the same gene family. If they are, genes are considered
tandemly duplicated and if they not not, then genes are not considered
tandemly duplicated
"""

import csv
import pandas as pd

FILE = 'Athaliana_447_Araport11.gene.gff3'
FILE2 = 'Orthogroups.txt'

genomic_structure = {}
genes_lst = []
with open(FILE, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[0].startswith('##'):
            continue
        if row[2] == 'gene':
            # row[0] -> chromosome location
            # row[3] and row[4] -> gene start and end location
            gene_id = row[-1].split('.')[0].split('=')[1]
            genes_lst.append(gene_id)
            if row[0] not in genomic_structure:
                genomic_structure[row[0]] = [[int(row[3]), int(row[4]), gene_id]]
            else:
                genomic_structure[row[0]].append([int(row[3]), int(row[4]), gene_id])                

# Test to ensure all genes in the .gff file are unique
if len(set(genes_lst)) != len(genes_lst):
    print('Duplicate genes detected')
            
for chromosome in genomic_structure:
     genomic_structure[chromosome].sort(key = lambda x : x[0])

# Assume all genes and orthogroups in this orthogroup file are
# unique, as an earlier script, process_og.py has already done this
ath_genes_og = {}
with open(FILE2, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Calculates orthogroup size for all species
        og = row[0].split(':')[0]
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        for a_gene in ath_genes:
            ath_genes_og[a_gene] = og
   
tandem_status = {}
no_orthogroups = []
for key in genomic_structure.keys():
    for index in range(len(genomic_structure[key]) - 1):
        gene = genomic_structure[key][index][2]
        if gene in ath_genes_og:
            gene_family = ath_genes_og[gene]
        else:
            no_orthogroups.append(gene)

        adj_index = index + 1
        adj_gene = genomic_structure[key][adj_index][2]
        if adj_gene in ath_genes_og:
            adj_gene_family = ath_genes_og[adj_gene]
        else:
            no_orthogroups.append(adj_gene)
        
        tandem_status[gene] = 0
        tandem_status[adj_gene] = 0
        
        if gene_family == adj_gene_family:
            tandem_status[gene] = 1
            tandem_status[adj_gene] = 1

tandem_status_df = pd.DataFrame.from_dict(
        tandem_status, orient='index', columns=['tan_tandem_dup'])
tandem_status_df.index.rename('Gene', inplace=True)
tandem_status_df.to_csv('edited_Ath_td.txt', sep='\t')

"""
# Number of genes with no orthogroups
len(no_orthogroups)
Out[8]: 0
"""
'''
tandem_status_df
Out[121]: 
           tan_tandem_dup
Gene                     
AT1G01010               0
AT1G01020               0
AT1G01030               0
AT1G01040               0
AT1G01050               0
                  ...
ATMG01350               0
ATMG01360               0
ATMG01370               0
ATMG01400               0
ATMG01410               0

[27655 rows x 1 columns]

# Eyeball data with notepad+ to ensure that 1s occur in >1 gene
'''