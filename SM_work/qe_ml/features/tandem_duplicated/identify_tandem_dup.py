# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:35:24 2019

@author: weixiong001

Gets the genomic structure json file and counts how many genes are tandemly
duplicated. Creates a df and prints it to a .csv file
"""

import json
import pandas as pd

with open('genomic_structure.json', 'r') as fp:
    genomic_structure = json.load(fp)

df = pd.read_csv('genefamily_data.hom.csv', sep='\t', 
                 names=['gf_id', 'species', 'gene_id'], comment='#')
df = df[df['species'] == 'ath']
# len(df['gene_id'].unique()) -> 27655, all genes here are unique

tandem_status = {}
for key in genomic_structure.keys():
    for index in range(len(genomic_structure[key]) - 1):        
        gene = genomic_structure[key][index][2]
        gene_family = df.loc[df['gene_id'] == gene, 'gf_id'].values[0]
        
        adj_index = index + 1
        adj_gene = genomic_structure[key][adj_index][2]
        adj_gene_family = df.loc[df['gene_id'] == adj_gene, 'gf_id'].values[0]
        
        tandem_status[gene] = 0
        tandem_status[adj_gene] = 0
        
        if gene_family == adj_gene_family:
            tandem_status[gene] = 1
            tandem_status[adj_gene] = 1
            
tandem_status_df = pd.DataFrame.from_dict(
        tandem_status, orient='index', columns=['tandem_dup'])
tandem_status_df.index.rename('genes', inplace=True)
# tandem_status_df.isna().any().any() -> False, no NAs
tandem_status_df.to_csv('genes_tandem_dup.csv', sep='\t')

# To see how many 0s and 1s there are
#tandem_status_df['tandem_dup'].value_counts()
#Out[8]: 
#0    25180
#1     2475
#Name: tandem_dup, dtype: int64
        