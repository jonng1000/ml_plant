# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:57:42 2022

@author: weixiong001
"""

import pandas as pd

FILE = 'G:/My Drive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
OUTPUT = 'draft_GO_100targets.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
filtered = df[df['Counts'] >= 100]

filtered.to_csv(OUTPUT, sep='\t')
