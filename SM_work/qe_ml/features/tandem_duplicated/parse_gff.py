# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:27:38 2019

@author: weixiong

Takes a .gff file, which is the genomic structure file and
creates a dict with has the location of all genes, sorted from start
to finish, according to increasing chromosome number
"""

import csv
import json

genomic_structure = {}
with open('Arabidopsis_thaliana.TAIR10.44.gff3', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        # len(row) >= 3 and row[2] -> selects for legit gene entries
        if len(row) >= 3 and row[2] == 'gene':
            # row[0] -> chromosome location
            # row[3] and row[4] -> gene start and end location
            # row[4]
            partial_processed = row[-1].split(';')[0]
            gene_id = partial_processed.split(':')[1]
            if row[0] not in genomic_structure:
                genomic_structure[row[0]] = [[int(row[3]), int(row[4]), gene_id]]
            else:
                genomic_structure[row[0]].append([int(row[3]), int(row[4]), gene_id])

for chromosome in genomic_structure:
     genomic_structure[chromosome].sort(key = lambda x : x[0])

     
# sanity check
c = 0
# c = 27655 genes, around the expected num of arabidopsis genes, and same
# num as that given in notepad++ when i count the num of araport11\tgene
# occurences
for chromosome in genomic_structure:
    c = c + len(genomic_structure[chromosome])

gene_lst = [positions[2] for chromosome in genomic_structure 
            for positions in genomic_structure[chromosome]]
# len(set(gene_lst)) -> 27655, which is the same as len(gene_lst), hence all
# genes are unique


with open('genomic_structure.json', 'w') as fp:
    json.dump(genomic_structure, fp, sort_keys=True, indent=4)

        