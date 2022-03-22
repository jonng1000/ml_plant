# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:46:11 2020

@author: weixiong001

Gets all parent and child terms for each GO term and then removes it
from the dataset
"""

import pandas as pd
from goatools import obo_parser

GO_FILE = 'D:\GoogleDrive\machine_learning\GO_labels'

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
# df is replaced by dataframe with only genes with experimental evidence
# codes
df = df.loc[df['Evidence'].isin(expt_evidence)]
set_GOs = set(df['GO_class'])  # 5192 unique GOs with experimental codes
dict_ans = {}
# Creates dict with GO class as key, and needed info as values
for each in set_GOs:
    go_term = go[each]
    children_itself = go_term.get_all_children()
    children_itself.add(each)
    selected =  df.loc[df['GO_class'].isin(children_itself)]
    set_genes = set(selected['Gene'])
    number = len(set_genes)
    str_genes = ' '.join(list(set_genes))
    if each in dict_ans:
        raise ValueError('GO class already found in dict!')
    dict_ans[each] = [number] + [go_term.namespace, go_term.name, str_genes]

# Converts dict to df and prints it
counts_df = pd.DataFrame.from_dict(dict_ans, orient='index',
                                   columns=['Counts', 'GO_domain', 'GO_desc',
                                            'Genes']
                                   )
counts_df.index.name = 'GO_class'
counts_df.to_csv('GO_gene_counts.txt', sep='\t')
