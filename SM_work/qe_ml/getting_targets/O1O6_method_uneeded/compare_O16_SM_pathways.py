# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:00:51 2019

@author: weixiong

Compating 2 methods of getting SM genes from AraCyc

Method 1: get all SM pathways, then get genes -> using below code:
SM_results = explore_SGM_genes('SM_class_aracyc.txt')

Method 2: get all pathways, then select SM pathways, then get genes ->
uses bulk of code below

Refer to "PhD notes ML gene prediction.docx" 23/7/19 for futher info
"""
import pandas as pd

###############################################################################
# Produces set of genes associated with SM pathways, but may not have
# experimental evidence
file = 'O1_O6_SM_genes.txt'

def explore_SGM_genes(file):
    gene_pathways = pd.read_csv(file, sep='\t')
    # return this
    desc_nan = gene_pathways.isna().sum()
    # return this
    num_nan = gene_pathways.isna().sum().sum()
    #nan means need to remove it before doing list comprehension below
    edited_pathways = gene_pathways.dropna()
    genes_pathways_series = edited_pathways['Genes of pathway'].str.split(' // ')
    genes_pathways_list = [one for row in genes_pathways_series for one in row]
    #return this
    list_genes_num = len(genes_pathways_list)
    # return this
    genes_pathways_set = set(genes_pathways_list)
    # return this, most important variable as its my SM genes
    num_genes = len(genes_pathways_set)
    return desc_nan, num_nan, list_genes_num, ('num_genes', num_genes), genes_pathways_set
###############################################################################

results = explore_SGM_genes(file)
#print(results[0])
#2 nan, 740 genes 

SM_results = explore_SGM_genes('SM_class_aracyc.txt')

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

alt_SM_expt_evid = results[4] & all_genes_set
len(alt_SM_expt_evid)  #271 genes

SM_expt_evid = SM_results[4] & all_genes_set
len(SM_expt_evid)  #254 genes
