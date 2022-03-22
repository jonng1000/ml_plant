# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:06:28 2019

@author: weixiong001

Takes all .gaf files downloaded from AmiGO, and identifies genes
belonging to GO terms secondary metabolic process and primary metaoblic
process, with experimental evidence. Then, write these genes into a .csv file.

Note: goa_uniprot_all_noiea.gaf.gz is not in the correct format so cannot be
read. Use another script to read it separately
"""

import pandas as pd
import csv
from Bio.UniProt.GOA import gafiterator
import os
import gzip
import time

'''
step 1: get all my go terms, convert to set
step 2: iterate thru all gzip files
step 3: for each gizp file, open and read line by file
step 4: each line, filter
step 5: write filtered line to a .csv file
'''
t0 = time.time()
# step 1: get all my go terms, convert to set
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

secondary_GOs = set(secondary_GOs) # length is same as length of its list
primary_GOs = set(primary_GOs)  # length is same as length of its list
expt_codes = {'EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP'}
# for step 5
with open('all_species_GO_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    # step 2: iterate thru all gzip files
    for file in os.listdir():
        if file.endswith('gz'):
            # step 3: for each gizp file, open and read line by file
            with gzip.open(file, 'rt') as handle:
                for rec in gafiterator(handle):
                    # step 4: each line, filter
                    gene, qualifier = rec['DB_Object_Symbol'], rec['Qualifier']
                    GO, evidence = rec['GO_ID'], rec['Evidence']
                    taxon = rec['Taxon_ID']
                    
                    if 'NOT' in qualifier:
                        continue
                    if evidence in expt_codes:
                        if GO in secondary_GOs or GO in primary_GOs:
                            if len(taxon) == 2:
                                taxon = [taxon[0]]           
                            row = [gene] + [GO] + [evidence] + taxon
                            # step 5: write filtered line to a .csv file
                            writer.writerow(row)
            print(file, 'done')
                
t1 = time.time()
total = t1-t0
# 3189 s -> 53 min
print('time taken', total, 'seconds')        
