# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 18:09:58 2022

@author: weixiong001

Calculating proportion of genes in GO domains according to specific criteria
"""

import pandas as pd
from goatools import obo_parser

# Reads in go.obo file with goatools
expt_evidence = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 
                 'HMP', 'HGI', 'HEP']
go_obo = 'go.obo'
go = obo_parser.GODag(go_obo)

# Reads in entire ATH GO Slim file
names_l = [i for i in range(16)]
df = pd.read_csv('ATH_GO_GOSLIM.txt', sep='\t', comment='!', names=names_l,
                 header=None)
df.rename(columns={0:'Gene', 3:'Relation', 4:'GO_desc', 5:'GO_class', 
                   7: 'GO_domain', 9:'Evidence'},
          inplace=True)


unique_values = df['Gene'].unique()
'''
# 31 301 genes
len(unique_values)
Out[39]: 31301
'''

gene_go_dom = df.loc[:, ['Gene', 'GO_domain']].drop_duplicates()
go_dom_count = gene_go_dom.groupby('GO_domain').size()

expt_df = df.loc[df['Evidence'].isin(expt_evidence)]
expt_gene_go_dom = expt_df .loc[:, ['Gene', 'GO_domain']].drop_duplicates()
expt_go_dom_count = expt_gene_go_dom.groupby('GO_domain').size()
