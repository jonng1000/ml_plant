# -*- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong
From mcl clustering output, 1HE clusters, calculates cluster size, and saves
this infomation in a file -> this script is for feature importance clusters
"""

import pandas as pd
import csv
FILE = 'dump.data.mci.I20'
OUTPUT = 'fi_clusters.txt'

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
df.index.name = 'Feature'
df = df.rename(columns={0: 'feat_cluster_id', 1: 'feat_cluster_size'})
'''
# Original number of features
df.shape
Out[178]: (1318, 2)
'''
expanded_df = pd.get_dummies(df, columns=['feat_cluster_id'])

'''
# After ohe of cluster ids, each feature should only belong to 1 cluster
# Hence summing all columns, shoudl give a value of 1 per feature
# Below code shows that its true
expanded_df.drop(columns=['feat_cluster_size']).sum(axis=1).unique()
Out[15]: array([1], dtype=int64)
'''
'''
# No nan exists
expanded_df.isnull().values.any()
Out[4]: False
'''
expanded_df.to_csv(OUTPUT, sep='\t')

