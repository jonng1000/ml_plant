# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 16:28:24 2019

@author: weixiong

Used to create venn diagrams for GO GM and SM gene sets.
Input data is my and the paper's data.
NOTE: Correct code for parsing GO data is not reflected here, probably forgot to
save the script. Will rerun and check it it within this week
"""

import pandas as pd
import csv

Ara_GO_targets = pd.read_csv('Ara_GO_targets.csv', sep='\t', index_col=0)
ds1s1 = pd.read_csv('d1s1_short.txt', sep='\t', index_col=0)

GO_GM = Ara_GO_targets[Ara_GO_targets['GO'] == 'GM']
GO_SM = Ara_GO_targets[Ara_GO_targets['GO'] == 'SM']
GO_GM_set = set(GO_GM.index)
GO_SM_set = set(GO_SM.index)
len(GO_GM_set)  # 1519
len(GO_SM_set)  # 121

ds1s1_GO_GM = ds1s1[ds1s1['GO_annotation'] == 'Primary metabolic process']
ds1s1_GO_SM = ds1s1[ds1s1['GO_annotation'] == 'Secondary metabolic process']
d_GO_GM_set = set(ds1s1_GO_GM.index)
d_GO_SM_set = set(ds1s1_GO_SM.index)
len(d_GO_GM_set)  # 1848
len(d_GO_SM_set)  # 233

len(GO_GM_set & d_GO_GM_set)  # 537
len(GO_GM_set - d_GO_GM_set)  # 982
len(d_GO_GM_set - GO_GM_set)  # 1311
len(GO_GM_set | d_GO_GM_set)  # 2830
# venn representation [982 [537] 1311]  # total is 2830 as well

len(GO_SM_set & d_GO_SM_set)  # 68
len(GO_SM_set - d_GO_SM_set)  # 53
len(d_GO_SM_set - GO_SM_set)  # 165
len(GO_SM_set | d_GO_SM_set)  # 286
# venn representation [53 [68] 165]  # total is 286 as well

with open('GO_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in GO_GM_set:
        writer.writerow([gene])
        
with open('GO_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in GO_SM_set:
        writer.writerow([gene])

with open('d_GO_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in d_GO_GM_set:
        writer.writerow([gene])
        
with open('d_GO_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in d_GO_SM_set:
        writer.writerow([gene])