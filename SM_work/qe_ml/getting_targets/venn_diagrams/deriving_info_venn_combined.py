# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 16:28:24 2019

@author: weixiong

Used to create venn diagrams for comparing: 
1) GM (my AraCyc and GO) and GM (paper's AraCyc and GO) gene sets
2) SM (my AraCyc and GO) and SM (paper's AraCyc and GO) gene sets
Input data is my and the paper's data.
"""

import pandas as pd
import csv

Ara_GO_targets = pd.read_csv('Ara_GO_targets.csv', sep='\t', index_col=0)
ds1s1 = pd.read_csv('d1s1_short.txt', sep='\t', index_col=0)

GO_GM = Ara_GO_targets[Ara_GO_targets['GO'] == 'GM']
ara_GM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'GM']
all_GM = set(GO_GM.index) | set(ara_GM.index)
len(all_GM)  # 2241

GO_SM = Ara_GO_targets[Ara_GO_targets['GO'] == 'SM']
ara_SM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'SM']
all_SM = set(GO_SM.index) | set(ara_SM.index)
len(all_SM)  # 207

ds1s1_GM = ds1s1[ds1s1['AraCyc_annotation'] == 'Non-secondary metabolism pathway']
ds1s1_GO_GM = ds1s1[ds1s1['GO_annotation'] == 'Primary metabolic process']
all_d_GM = set(ds1s1_GM.index) | set(ds1s1_GO_GM.index)
len(all_d_GM)  # 2501

ds1s1_SM = ds1s1[ds1s1['AraCyc_annotation'] == 'Secondary metabolism pathway']
ds1s1_GO_SM = ds1s1[ds1s1['GO_annotation'] == 'Secondary metabolic process']
all_d_SM = set(ds1s1_SM.index) | set(ds1s1_GO_SM.index)
len(all_d_SM)  # 602

len(all_GM & all_d_GM)  # 965
len(all_GM - all_d_GM)  # 1176
len(all_d_GM - all_GM)  # 1536
len(all_GM | all_d_GM)  # 3677
# venn representation [1176 [965] 1536]  # total is 3677 as well

len(all_SM & all_d_SM)  # 140
len(all_SM - all_d_SM)  # 67
len(all_d_SM - all_SM)  # 462
len(all_SM | all_d_SM)  # 669
# venn representation [67 [140] 462]  # total is 669 as well

with open('all_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in all_GM:
        writer.writerow([gene])
        
with open('all_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in all_SM:
        writer.writerow([gene])

with open('all_d_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in all_d_GM:
        writer.writerow([gene])
        
with open('all_d_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in all_d_SM:
        writer.writerow([gene])
        
