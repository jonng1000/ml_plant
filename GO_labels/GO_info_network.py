# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 22:49:28 2021

@author: weixiong001

Creating a file with GO descriptions for feature importance network
analysis.

Produces GO_info_network.txt
"""

import pandas as pd

FILE = 'sort_GO_gene_counts.txt'
OUTPUT = 'GO_info_network.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

df['GO_info'] = 'GO_' + df['GO_domain'] + '_' + df['GO_desc']

selected = df.loc[:, ['GO_info', 'GO_domain', 'GO_desc']]
selected.index = 'go_' + selected.index

selected.to_csv(OUTPUT, sep='\t')