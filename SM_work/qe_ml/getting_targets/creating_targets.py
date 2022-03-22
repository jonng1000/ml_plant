# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:48:31 2019

@author: weixiong

Creating list of targts - GM (Aracyc + GO) only and SM (Aracyc + GO) only 
Genes labelled w both GM and SM from Aracyc and GO data sets are not
included
"""

import pandas as pd
import csv

Ara_GO_targets = pd.read_csv('Ara_GO_targets.csv', sep='\t', index_col=0)

AC_GM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'GM']
GO_GM = Ara_GO_targets[Ara_GO_targets['GO'] == 'GM']
all_GM = set(GO_GM.index) | set(AC_GM.index)
len(all_GM)  # 2241

GO_SM = Ara_GO_targets[Ara_GO_targets['GO'] == 'SM']
ara_SM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'SM']
all_SM = set(GO_SM.index) | set(ara_SM.index)
len(all_SM)  # 207

only_GM = all_GM - all_SM
only_SM = all_SM - all_GM

with open('only_GM_targetsv2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in only_GM:
        writer.writerow([gene])
        
with open('only_SM_targetsv2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in only_SM:
        writer.writerow([gene])