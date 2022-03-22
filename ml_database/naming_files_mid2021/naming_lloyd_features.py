# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:23:23 2021

@author: weixiong001

Assign type and description names to features for database
"""

import pandas as pd

FILE = '/mnt/d/GoogleDrive/machine_learning/ml_go_workflow/all_data/lloyd_features.txt'
OUTPUT = 'lloyd_features_info.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

# Create df with required info
temp = df.columns.to_frame(index=False)
df = temp.rename({0: 'ID'}, axis='columns')

# Different prefixes here, so this allows me to see all of them
'''
>>> set(df['ID'].str.split('_').str[0])
{'con', 'gbm', 'ntd'}
'''

# Temp list for Type column
dNdS_feat = ['Conservation (con)'] * 4
dS_para_feat = ['Conservation (con)']
per_id_feat = ['Conservation (con)']
seq_conv_feat = ['Conservation (con)'] * 3
nt_div_feat = ['Evolution (ntd)']
gene_meth_feat = ['Epigenetics (gbm)']
lst_values = dNdS_feat + dS_para_feat + per_id_feat + seq_conv_feat + nt_div_feat + gene_meth_feat
df.insert(loc=0, column='Type', value=lst_values)

# Temp list for Description column
dNdS_feat = ['Nonsynonymous (dN)/synonymous (dS) substitution rates (also called ka/ks)  between A. thaliana paralogs, and homologs from 5 plant species'] * 4
dS_para_feat = ['dS with putative paralog']
per_id_feat = ['Maximum percent identity from BLAST to closest paralog']
seq_conv_feat = ['Protein sequence % identity (ID) to fungi, plants, metazoans'] * 3
nt_div_feat = ['Nucleotide diversity calculated among 80 A. thaliana accessions']
gene_meth_feat = ['Whether gene body is methlyated']
lst_values = dNdS_feat + dS_para_feat + per_id_feat + seq_conv_feat + nt_div_feat + gene_meth_feat
df.insert(loc=2, column='Description', value=lst_values)

df.to_csv(OUTPUT, sep='\t', index=False)
