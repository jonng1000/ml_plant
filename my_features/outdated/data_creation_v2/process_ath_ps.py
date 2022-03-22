# -*- coding: utf-8 -*-
"""
Created on 230620

@author: weixiong

Takes in the phylostrata file from Marek (who got it from Irene), selects
for Arabidopsis genes, and converts their phylostrata into features via
one hot encoding, and saves the result in a file.
"""

import pandas as pd

FILE = 'gene2node.txt'
OUTPUT = 'edited_Ath_ps.txt'

df = pd.read_csv(FILE, sep='\t', names=['phylostrata'], index_col=0)
df.index.name = 'Gene'
'''
# Number of unique phylostrata across all species
len(df['phylostrata'].unique())
Out[35]: 41
'''

ath_df = df.loc[df.index.str.startswith('AT'), :]
new_gene_names = {name: name.split('-')[0] for name in ath_df.index}
renamed_ath_df = ath_df.rename(new_gene_names, axis='index')
'''
# No missing values in dataframe
renamed_ath_df.isnull().values.any()
Out[31]: False
'''

dict_replace = {}
for node in renamed_ath_df['phylostrata'].unique():
    if node == 'ARATH':
        dict_replace[node] = 18
    else:
        dict_replace[node] = int(node.split('_')[1])

renamed_ath_df['phylostrata'] = renamed_ath_df['phylostrata'].\
                                replace(dict_replace)
renamed_ath_df = renamed_ath_df.rename(columns={'phylostrata': 'phy_phylostrata'})

'''
# Number of Arabidopsis genes
renamed_ath_df.shape
Out[36]: (27382, 1)
'''
renamed_ath_df.to_csv(OUTPUT, sep='\t')
