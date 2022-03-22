# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 16:28:24 2019

@author: weixiong

Used to create venn diagrams for AraCyc GM and SM gene sets.
Input data is my and the paper's data.
"""

import pandas as pd
import csv

Ara_GO_targets = pd.read_csv('Ara_GO_targets.csv', sep='\t', index_col=0)
ds1s1 = pd.read_csv('d1s1_short.txt', sep='\t', index_col=0)

AC_GM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'GM']
AC_SM = Ara_GO_targets[Ara_GO_targets['AraCyc'] == 'SM']
AC_GM_set = set(AC_GM.index)
AC_SM_set = set(AC_SM.index)
len(AC_GM_set)  # 924
len(AC_SM_set)  # 110

ds1s1_GM = ds1s1[ds1s1['AraCyc_annotation'] == 'Non-secondary metabolism pathway']
ds1s1_SM = ds1s1[ds1s1['AraCyc_annotation'] == 'Secondary metabolism pathway']
d_GM_set = set(ds1s1_GM.index)
d_SM_set = set(ds1s1_SM.index)
len(d_GM_set)  # 1306
len(d_SM_set)  # 423

len(AC_GM_set & d_GM_set)  # 497
len(AC_GM_set - d_GM_set)  # 427
len(d_GM_set - AC_GM_set)  # 809
len(AC_GM_set | d_GM_set)  # 1733
# venn representation [427 [497] 809]  # total is 1733 as well

len(AC_SM_set & d_SM_set)  # 81
len(AC_SM_set - d_SM_set)  # 29
len(d_SM_set - AC_SM_set)  # 342
len(AC_SM_set | d_SM_set)  # 452
# venn representation [29 [81] 342]  # total is 452 as well

with open('AC_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in AC_GM_set:
        writer.writerow([gene])
        
with open('AC_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in AC_SM_set:
        writer.writerow([gene])

with open('d_GM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in d_GM_set:
        writer.writerow([gene])
        
with open('d_SM_venn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for gene in d_SM_set:
        writer.writerow([gene])