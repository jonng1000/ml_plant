# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 18:51:35 2021

@author: weixiong001

Add GO top level domain names to GO scores 
"""

import pandas as pd

GO_PATH = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
FILE = 'go_scores.txt'
OUTPUT = 'go_scores_domains.txt'

df = pd.read_csv(GO_PATH, sep='\t', index_col=0)
df2 =  pd.read_csv(FILE, sep='\t', index_col=0)

df.index = df.index.str.replace('GO:', 'go_GO_')
combine = pd.concat([df2, df['GO_domain']], join='inner', axis=1)
selected = combine.loc[:, ['GO_domain', 'oob_f1']]
selected.index.name = 'class label'

selected.to_csv(OUTPUT, sep='\t')




