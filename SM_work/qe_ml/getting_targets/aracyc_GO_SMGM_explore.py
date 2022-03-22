# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:30:41 2019

@author: weixiong
"""
import csv
import pandas as pd

with open('Aracyc_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        aracyc_GM = set(row) 
        #len(aracyc_GM) # 924
        
with open('Aracyc_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        aracyc_SM = set(row) 
        #len(aracyc_SM) # 110

with open('GO_GM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        GO_GM = set(row) 
        #len(GO_GM) # 1519
        
with open('GO_SM_only.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        GO_SM = set(row) 
        #len(GO_SM) # 121
        
# =============================================================================
# Results of set operations on these sets
# len(aracyc_GM & GO_GM) # Inserection
# Out[2]: 302
# 
# len(aracyc_SM & GO_SM)
# Out[3]: 24
# 
# len(aracyc_GM | GO_GM) # Union
# Out[4]: 2141
# 
# len(aracyc_SM | GO_SM)
# Out[5]: 207
# =============================================================================
        
# some genes not found in one or the other databases
# or annotated as not experimental but it is in the other

# weird gene names? PAD1 (TAIR)? G-1082 (Ara-Cyc)? Need to convert to
# AT.... format if there's too many
        
aracyc_GM_ATformat = [i for i in aracyc_GM if not i.startswith('AT')]
aracyc_SM_ATformat = [i for i in aracyc_SM if not i.startswith('AT')]
GO_GM_ATformat = [i for i in GO_GM if not i.startswith('AT')]
GO_SM_ATformat = [i for i in GO_SM if not i.startswith('AT')]

a_GM_percent_wrong = len(aracyc_GM_ATformat)/len(aracyc_GM) * 100  # 1.08%
a_SM_percent_wrong = len(aracyc_SM_ATformat)/len(aracyc_SM) * 100  # 1.82%
GO_GM_percent_wrong = len(GO_GM_ATformat)/len(GO_GM) * 100  # 1.78%
GO_SM_percent_wrong = len(GO_SM_ATformat)/len(GO_SM) * 100  # 4.13%

# =============================================================================
# This section creates a dataframe containing genes with their GM/SM
# classification from AraCyc and GO databases

# Creates dict
aracyc_union = aracyc_GM | aracyc_SM
ara_dict = {}
for gene in aracyc_union:
    if gene in ara_dict:
        print(gene, 'present')
        break
    else:
        if gene in aracyc_GM and gene in aracyc_SM:
            print(gene, 'present in both')
            break
        elif gene in aracyc_GM:
            ara_dict[gene] = ['GM']
        elif gene in aracyc_SM:
            ara_dict[gene] = ['SM']
        else:
            print('gene not found')
            break

GO_union = GO_GM | GO_SM
GO_dict = {}
for gene in GO_union:
    if gene in GO_dict:
        print(gene, 'present')
        break
    else:
        if gene in GO_GM and gene in GO_SM:
            print(gene, 'present in both')
            break
        elif gene in GO_GM:
            GO_dict[gene] = ['GM']
        elif gene in GO_SM:
            GO_dict[gene] = ['SM']
        else:
            print('gene not found')
            break     
        
aracyc_df = pd.DataFrame.from_dict(ara_dict, orient='index', columns=['AraCyc'])
GO_df = pd.DataFrame.from_dict(GO_dict, orient='index', columns=['GO'])
# Missing values are listed as nan
combined_df = pd.concat([aracyc_df, GO_df], axis=1)
len(combined_df)  # 2294 genes
len(aracyc_GM | aracyc_SM | GO_GM | GO_SM)  # 2294
# Above shows that combined_df has the correct num of genes
all_genes_not_ATformat = [
        i for i in combined_df.index if not i.startswith('AT')
        ]
# 1.87% genes does not start with AT....
len(all_genes_not_ATformat)/len(combined_df.index) * 100

combined_df.to_csv('Ara_GO_targets.csv', 
                   sep='\t', na_rep='NA', index_label='Gene')
