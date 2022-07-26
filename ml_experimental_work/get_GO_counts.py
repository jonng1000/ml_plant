# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:29:39 2022

@author: weixiong001

Initially to create expt GO terms as targets for ml, but got error so decided
not to continue this
"""

import pandas as pd
from goatools import obo_parser

FILE = './tair_gaf/tair.gaf'
OUTPUT = 'atg_GO_features.txt'
OUTPUT2 = 'AT1G04250_GO_features.txt'
OUTPUT3 = 'atg_GO_features_corrected.txt'

go_obo = 'go.obo'
go = obo_parser.GODag(go_obo)

names_l = [i for i in range(17)]
df = pd.read_csv(FILE, sep='\t', comment='!', names=names_l,
                 header=None)
df.rename(columns={0:'DB', 1: 'DB Object ID', 2:'DB Object Symbol', 
                   3:'Qualifier', 4:'GO ID', 6:'Evidence Code', 
                   8: 'Aspect'},
          inplace=True)
atg_names = df.loc[df['DB Object ID'].str.contains('^AT[1-5|M|C]G[0-9]{4}[0-9]$', regex=True), :]

expt_evidence = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 
                 'HMP', 'HGI', 'HEP']
atg_names = atg_names.loc[df['Evidence Code'].isin(expt_evidence)]
selected_df = atg_names.loc[:, ['DB Object ID', 'GO ID']]

set_GOs = set(selected_df['GO ID'])  # 5448 unique GOs with experimental codes
dict_ans = {}
# Creates dict with GO class as key, and needed info as values
for each in set_GOs:
    go_term = go[each]
    children_itself = go_term.get_all_children()
    children_itself.add(each)
    selected =  selected_df.loc[selected_df['GO ID'].isin(children_itself)]
    set_genes = set(selected['DB Object ID'])
    number = len(set_genes)
    str_genes = ' '.join(list(set_genes))
    if each in dict_ans:
        raise ValueError('GO class already found in dict!')
    dict_ans[each] = [number] + [go_term.namespace, go_term.name, str_genes]