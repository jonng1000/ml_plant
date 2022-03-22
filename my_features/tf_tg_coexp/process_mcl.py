# -*- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong
From mcl clustering output, 1HE clusters, calculates cluster size, and saves
this infomation in a file -> this script is for tf-tg gene reg network clusters.
Only takes clusters with >1 gene
"""

import pandas as pd
import csv
FILE = 'dump.data.mci.I20'
OUTPUT = 'ath_ttr_clusters.txt'

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
df = df.rename(columns={0: 'tti_cluster_id', 1: 'ttr_cluster_size'})
'''
# Original number of features
df.shape
Out[178]: (15852, 2)
'''
filtered_df = df.loc[df['ttr_cluster_size'] > 1, :]
filtered_df = pd.get_dummies(filtered_df, columns=['tti_cluster_id'])

'''
# After ohe of cluster ids, each gene should only belong to 1 cluster
# Hence summing all columns, shoudl give a value of 1 per gene
# Below code shows that its true
filtered_df.drop(columns=['ttr_cluster_size']).sum(axis=1).unique()
Out[15]: array([1], dtype=int64)
'''
'''
# No nan exists
filtered_df.isnull().values.any()
Out[4]: False
'''

'''
filtered_df.shape
Out[192]: (15851, 55)
'''
filtered_df.to_csv(OUTPUT, sep='\t')

