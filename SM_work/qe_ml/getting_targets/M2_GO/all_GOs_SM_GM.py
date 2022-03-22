# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:37:06 2019

@author: weixiong

This script takes in the .csv files with the relevant GO terms and uses it to select for the
correct genes in the TAIR GO file (ATH_GO_GOSLIM.txt).
"""

import csv

lst_expt_evidence = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP']

###############################################################################
with open('all_children_GO0019748.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        SM_GOs = set(row)

lst_genes = []
with open('ATH_GO_GOSLIM.txt', newline='') as csvfile:
    reader2 = csv.reader(csvfile, delimiter='\t')
    # row[0] -> gene
    # row[5] -> GO term
    # row[9] -> evidence code
    for row in reader2:
        if row[5] in SM_GOs and row[9] in lst_expt_evidence:
            lst_genes.append(row[0])
    unique_genes_SM = set(lst_genes)
    len(unique_genes_SM) # 138 genes
###############################################################################

###############################################################################
with open('all_children_GO0044238.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        GM_GOs = set(row)

lst_genes = []
with open('ATH_GO_GOSLIM.txt', newline='') as csvfile:
    reader2 = csv.reader(csvfile, delimiter='\t')
    # row[0] -> gene
    # row[5] -> GO term
    # row[9] -> evidence code
    for row in reader2:
        if row[5] in GM_GOs and row[9] in lst_expt_evidence:
            lst_genes.append(row[0])
    unique_genes_GM = set(lst_genes)
    len(unique_genes_GM) # 1536 genes
    
###############################################################################

dual_genes = unique_genes_SM & unique_genes_GM
len(dual_genes) #17
only_SM_expt_evid = unique_genes_SM - dual_genes
len(only_SM_expt_evid) #121
only_GM_expt_evid = unique_genes_GM - dual_genes
len(only_GM_expt_evid) #1519

with open('GO_SM_only.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(list(only_SM_expt_evid))
    
with open('GO_GM_only.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(list(only_GM_expt_evid))
