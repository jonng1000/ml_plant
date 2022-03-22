# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:33:32 2020

@author: weixiong001

Permutation test, to test for enrichment/depletion of GO terms in coexp clusters
"""

import pandas as pd
import sys

# Input 
GO_TERM = sys.argv[1] #'cytosol'
# Replaces _ with space, as GO terms has this instead
GO_TERM = GO_TERM.replace('_', ' ')
CLUSTER = sys.argv[2] #'cid_cluster_id_114'
NUM = 1000
# Locations of files
FOLDER = '/mnt/d/GoogleDrive/machine_learning/my_features/coexp_network/'
FILE = 'ath_coe_clusters.txt'
GO_FILE = '/mnt/d/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
ML_FILE = '/mnt/d/GoogleDrive/machine_learning/my_features/ml_runs_v2/ml_16l_edited.txt'

# Reading in files
file_path = FOLDER + FILE
df = pd.read_csv(file_path, sep='\t', index_col=0)
go_df = pd.read_csv(GO_FILE, sep='\t', index_col=0)
# Reads in only index, empty df with gene names as index
ml_df = pd.read_csv(ML_FILE, sep='\t', index_col=0, usecols=[0])

# Specific cluster
specific_cluster = df.loc[df[CLUSTER] == 1, CLUSTER]
gene_names = specific_cluster.index
num_genes = len(specific_cluster)

# Genes in a specific GO term
go_term_genes = go_df.loc[go_df['GO_desc'] == GO_TERM, 'Genes']
gtg_set = set(go_term_genes.iloc[0].split(' '))
'''
# Just to check that there's no duplicate genes here
len(go_term_genes.iloc[0].split(' ')) ==\
len(set(go_term_genes.iloc[0].split(' ')))
Out[150]: True
'''


def cal_prop(names, set_names, num_g):
    """
    Calculate proportion of genes in a cluster, with a specific go term
    """
    c = 0
    for gene in names:
        if gene in set_names:
            c += 1
    prop = c / num_g
    return prop


orig_prop = cal_prop(gene_names, gtg_set, num_genes)

count = 0
for i in range(NUM):
    ran_sel = ml_df.sample(num_genes).index
    new_prop = cal_prop(ran_sel, gtg_set, num_genes)
    if orig_prop > new_prop:
        count += 1

prop_greater = count / NUM
p_value = 1 - prop_greater
# First value is fraction of times where orig proportion is greater than random
# proportion, and second value is the p-value of its significance
print(prop_greater, p_value)
