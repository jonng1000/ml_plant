# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:57:23 2019

@author: weixiong
"""

import pandas as pd

############################################################################### 
SM_file = 'SM_class_aracyc.txt'
SM_pathways = pd.read_csv(SM_file, sep='\t')
#SM_pathways.isna().sum().sum()
#Only 1 nan, PWY-5349 has no genes
#nan means need to remove it before doing list comprehension below
SM_edited_pathways = SM_pathways.dropna()
SM_all_pathways_series = SM_edited_pathways['Genes of pathway'].str.split(' // ')
SM_all_pathways_list = [one for row in SM_all_pathways_series for one in row]
# 1057 genes in all_pathways_list, secondary metabolism
SM_all_pathways_set = set(SM_all_pathways_list)
len(SM_all_pathways_set) # 660 genes
############################################################################### 

############################################################################### 
GM_file = 'GM_class_aracyc.txt'
GM_pathways = pd.read_csv(GM_file, sep='\t')
#GM_pathways.isna().sum().sum()
#7 nan, 7 pathways has no genes
#nan means need to remove it before doing list comprehension below
GM_edited_pathways = GM_pathways.dropna()
GM_all_pathways_series = GM_edited_pathways['Genes of pathway'].str.split(' // ')
GM_all_pathways_list = [one for row in GM_all_pathways_series for one in row]
# 4453 genes in all_pathways_list, secondary metabolism
###############################################################################

all_file = 'all_pathways_aracyc.txt'
all_pathways = pd.read_csv(all_file, sep='\t')

for column in all_pathways.iloc[:,2:].columns:
    test = all_pathways[all_pathways[column].str.contains("SECONDARY-METABOLITE-BIOSYNTHESIS")]

