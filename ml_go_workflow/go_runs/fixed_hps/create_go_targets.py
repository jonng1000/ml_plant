# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:57 2021

@author: weixiong001

Creates a list of GO class labels, to use for my ml workflow. Min class size
is 10 genes
"""

import pandas as pd

FILE = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
OUTPUT = 'class_labels_go.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
# To get GO class name as a column
df = df.loc[df['Counts'] >= 10, :].reset_index()

df.to_csv(OUTPUT, sep='\t', columns=['GO_class'], header=False, index=False)