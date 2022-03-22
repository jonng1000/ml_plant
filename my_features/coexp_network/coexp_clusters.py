# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:05:33 2020

@author: weixiong001

Takes in Marek's ouput from his HCCA script (gene coexpression clusters), and
OHE cluster ids (excludes gene clusters with <5 genes), and calculates cluster
sizes. OHE clusters ids and cluster sizes are saved into a file as the output. 
"""

import csv
import numpy as np
import pandas as pd

FILE = 'clustering_method_1.tab'
OUTPUT = 'ath_coe_clusters.txt'

# Just to check that the first column in file is all 1s, and that all cluster
# ids are unique 
# Probably can skip this code section if I want
clusters_id_set = set()
with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for row in csvreader:
        if row[0] == '1':
            pass
        else:
            print('Not string 1')
        if row[1] not in clusters_id_set:
            clusters_id_set.add(row[1])
        else:
            print('Repeated cluster id seen')

# Actual processing of coexpression clusters
cluster_dict = {}
with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for row in csvreader:
        cluster_id = row[1].split('_')[-1]
        # Replace ; to add space, then ) as the last gene has this, so need
        # to remove it
        genes_str = row[2].replace('(', ' ').replace(';', ' ').replace(')', '')
        all_genes = set(genes_str.split(' '))
        cluster_size = len(all_genes)
        # Only take cluster ids if its size is >= 5
        if cluster_size >= 5:
            for gene in all_genes:
                if gene not in cluster_dict:
                    cluster_dict[gene] = [cluster_id, cluster_size]
                else:
                    print(gene, 'already present!')
        # Ignore cluster id if its size is <5
        else:
            for gene in all_genes:
                if gene not in cluster_dict:
                    cluster_dict[gene] = [np.nan, cluster_size]
                else:
                    print(gene, 'already present!')

df = pd.DataFrame.from_dict(cluster_dict, orient='index')
df.index.name = 'Gene'
df = df.rename(columns={0: 'cid_cluster_id', 1: 'coe_cluster_size'})  
'''
# Number of genes with each feature
df['coe_cluster_size'].count()
Out[55]: 24938
df['cid_cluster_id'].count()
Out[56]: 24526
'''
df = pd.get_dummies(df, columns=['cid_cluster_id'])
'''
# Original number of clusters
len(clusters_id_set)
Out[47]: 463
# Number of clusters, igoring clusters with < 5 genes
len(df.columns)-1
Out[51]: 278
# About 200 clusters have < 5 genes
'''
df.to_csv(OUTPUT, sep='\t')