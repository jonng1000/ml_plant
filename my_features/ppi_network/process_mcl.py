# -*- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong
From mcl clustering output, 1HE ppi clusters, calculates cluster size, and saves
this infomation in a file. Only takes clusters with >1 gene
"""

import pandas as pd
import csv
# Loading complete biogrid database, all species
FILE = 'dump.data.mci.I20'
OUTPUT = 'ath_ppi_clusters.txt'

with open(FILE, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    cluster_dict = {}
    cluster_id = 0
    for row in csv_reader:
        cluster_id += 1
        cluster_size = len(row)
        for gene in row:
            if gene not in cluster_dict:
                cluster_dict[gene] = [cluster_id, cluster_size]
            else:
                print(gene, 'already present!')

df = pd.DataFrame.from_dict(cluster_dict, orient='index')
df.index.name = 'Gene'
df = df.rename(columns={0: 'pid_cluster_id', 1: 'ppi_cluster_size'})
'''
df.shape
Out[200]: (10585, 2)
'''
filtered_df = df.loc[df['ppi_cluster_size'] > 1, :]
'''
filtered_df.shape
Out[201]: (10352, 2)
'''
filtered_df = pd.get_dummies(filtered_df, columns=['pid_cluster_id'])

'''
# After ohe of cluster ids, each gene should only belong to 1 cluster
# Hence summing all columns, shoudl give a value of 1 per gene
# Below code shows that its true
filtered_df.drop(columns=['ppi_cluster_size']).sum(axis=1).unique()
Out[207]: array([1], dtype=int64)
'''
'''
# No nan exists
filtered_df.isnull().values.any()
Out[4]: False
'''

filtered_df.to_csv(OUTPUT, sep='\t')

