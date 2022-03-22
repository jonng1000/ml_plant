# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

Takes in a processed fasta file (no decimals in gene ids, no * at the end of
sequences), and counts the length of each peptide, and outputs a dataframe
with this info
"""

import pandas as pd
from Bio import SeqIO

PATH = 'D:/GoogleDrive/machine_learning/my_features/interpro_files/'
FILE = PATH + 'ath_aa_processed.fa'
OUTPUT = 'aa_length.txt'

genes_dict = {}
with open(FILE) as original:
    records = SeqIO.parse(FILE, 'fasta')
    for record in records:
        if record.id not in genes_dict:
            genes_dict[record.id] = len(record.seq)
        else:
            print(record.id, 'already exists!')

'''
# Exploring results            
min(genes_dict.values())
Out[24]: 3

max(genes_dict.values())
Out[25]: 5400

for k,v in genes_dict.items():
    if v == 3:
        print(k)
        
AT2G21105
'''

aal_df = pd.DataFrame.from_dict(genes_dict, orient='index')
aal_df.rename(columns={0: 'pep_aal'}, inplace=True)
aal_df.index.name = 'Genes'

aal_df.to_csv(OUTPUT, sep='\t')

'''
aal_df
Out[196]: 
           pep_aal
Genes             
ATCG00500      488
ATCG00510       37
ATCG00280      473
ATCG00890      389
ATCG01250      389
           ...
AT5G39100      222
AT5G58460      857
AT5G46874       79
AT5G47240      398
AT5G52115      127

[27654 rows x 1 columns]
'''
