# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:02:22 2019

@author: weixiong
"""

import csv
from goatools import obo_parser

go_obo = 'go.obo'
go = obo_parser.GODag(go_obo)
go_id = 'GO:0044238'
go_term = go[go_id]
#print(go_term)

children = go_term.get_all_children()
print(len(children), type(children))
list_children = list(children)
list_children.append('GO:0044238')  # parent term is not added by default
#print(list_children[0:50])

with open('all_children_GO0044238.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(list_children)