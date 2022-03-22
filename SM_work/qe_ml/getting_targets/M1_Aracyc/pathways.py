# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:57:23 2019

@author: weixiong
"""

import pandas as pd
import csv

###############################################################################
# Produces set of genes associated with SM pathways, but may not have
# experimental evidence
SM_file = 'SM_class_aracyc.txt'
SM_pathways = pd.read_csv(SM_file, sep='\t')
#SM_pathways.isna().sum().sum()
#Only 1 nan, PWY-5349 has no genes
#nan means need to remove it before doing list comprehension below
SM_edited_pathways = SM_pathways.dropna()
SM_all_pathways_series = SM_edited_pathways['Genes of pathway'].str.split(' // ')
SM_all_pathways_list = [one for row in SM_all_pathways_series for one in row]
# 1057 genes in all_pathways_list, secondary metabolism
SM_all_pathways_set = set(SM_all_pathways_list)
len(SM_all_pathways_set) # 660 genes
############################################################################### 

###############################################################################
# Produces set of genes associated with GM pathways, but may not have
# experimental evidence 
GM_file = 'GM_class_aracyc.txt'
GM_pathways = pd.read_csv(GM_file, sep='\t')
#GM_pathways.isna().sum().sum()
#7 nan, 7 pathways has no genes
#nan means need to remove it before doing list comprehension below
GM_edited_pathways = GM_pathways.dropna()
GM_all_pathways_series = GM_edited_pathways['Genes of pathway'].str.split(' // ')
GM_all_pathways_list = [one for row in GM_all_pathways_series for one in row]
# 4453 genes in all_pathways_list, secondary metabolism
GM_all_pathways_set = set(GM_all_pathways_list)
len(GM_all_pathways_set) # 2609 genes
###############################################################################

###############################################################################
# Produces set of all genes associated with experimental evidence
all_genes_file = 'all_genes.txt'
all_genes = pd.read_csv(all_genes_file, sep='\t')
#all_genes.isna().sum().sum()
#26 nan for gene names
edited_genes = all_genes.dropna()
all_genes_series = edited_genes['Gene Name'].str.split(' // ')
all_genes_list = [one for row in all_genes_series for one in row]
# 1416 genes in all_genes_list, expt evidence
all_genes_set = set(all_genes_list)
len(all_genes_set) # 1375 genes
###############################################################################

###############################################################################
# Produces set of SM genes associated with experimental evidence
diff_SM_all = SM_all_pathways_set - all_genes_set
len(diff_SM_all)  #406 genes
SM_expt_evid = SM_all_pathways_set & all_genes_set
len(SM_expt_evid)  #254 genes
###############################################################################

###############################################################################
# Produces set of GM genes associated with experimental evidence
diff_GM_all = GM_all_pathways_set - all_genes_set
len(diff_GM_all)  #1541 genes
GM_expt_evid = GM_all_pathways_set & all_genes_set
len(GM_expt_evid)  #1068 genes
###############################################################################

dual_genes = SM_expt_evid & GM_expt_evid
len(dual_genes) #144
only_SM_expt_evid = SM_expt_evid - dual_genes
len(only_SM_expt_evid) #110
only_GM_expt_evid = GM_expt_evid - dual_genes
len(only_GM_expt_evid) #924

with open('Aracyc_SM_only.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(list(only_SM_expt_evid))
    
with open('Aracyc_GM_only.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(list(only_GM_expt_evid))