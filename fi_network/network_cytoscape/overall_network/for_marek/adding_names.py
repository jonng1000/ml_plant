# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 16:56:53 2021

@author: weixiong001
"""

import pandas as pd
import numpy as np

FILE = 'orginal_node_names.csv'
FILE2 = 'GO_info_network.txt'
OUTPUT = 'new_names.txt'

df = pd.read_csv(FILE, sep=',', index_col=0)
df = df.reset_index()
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)

selected = df.loc[:, ['expt_name', 'shared_name']]
selected.insert(0, 'new_name', np.nan)
selected['new_name'] = np.where(~selected['expt_name'].isna(), 
                                selected['expt_name'], selected['new_name'])
selected = selected.set_index('shared_name')

selected2 = df2.loc[:, 'GO_info']

combined = pd.concat([selected, selected2], axis=1)
combined['new_name'] = np.where(~combined['GO_info'].isna(), 
                                combined['GO_info'], combined['new_name'])
combined['new_name'] = np.where(combined['new_name'].isna(), 
                                combined.index, combined['new_name'])
combined.index.name = 'shared_name'

combined.to_csv(OUTPUT, sep='\t')
