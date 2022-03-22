# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

Checks to make sure my GO terms and genes associated with it makes sense,
creates many data files from the main ml data file (where each new file is
split into two classes, genes in GO term and genes not in GO term), also
creates a records.txt file which shows each of these two classes, and their
gene counts.


"""
import pandas as pd
import numpy as np

GO_SELECT = 'D:/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'
ML_DATA = "fully_processed_suba.txt"
CLASS_LABELS = 'AraCyc annotation'

colnames=['GO class', 'number', 'GO cat', 'GO name', 'genes'] 
selection = pd.read_csv(GO_SELECT, sep="\t", names=colnames, header=None)

##############################################################################
# Does some basic data exploration and checkking
dict_GO = {}
# Checks that GO counts equals the number of genes, and list of genes has no
# repeats. No exception raised, hence its fine
for index, row in selection.iterrows():
    count = row['number']
    lst = row['genes'].split()
    if count != len(lst):
        raise ValueError('GO counts is not equal to number of genes')
    g_set = set(lst)
    if len(g_set) != len(lst):
        raise ValueError('Genes have repeats')
    dict_GO[row['GO name']] = g_set

# Checks to see if GO terms have gene sets which are mutually exclusive
ans = []
for i in dict_GO.keys():
    for j in dict_GO.keys():
        if i == j:
            continue
        status = dict_GO[i].isdisjoint(dict_GO[j])
        ans.append([i, j, status])

# No pairwise comparision of GO terms are printed, which means that
# all GO terms have gene sets which are mutually exclusive
for sublist in ans:
    if sublist[2] == True:
        print(sublist)

total_genes = selection['number'].sum()

##############################################################################
# Divides genes into two classes based on GO terms
def get_classes(go_dict, pos_class):
    neg_class = 'not ' + pos_class
    gene_set = set()
    for k in go_dict.keys():
        if k != pos_class:
            gene_set = gene_set | go_dict[k]
    inter = gene_set & go_dict[pos_class]
    not_k = gene_set - inter
    class_dict = {pos_class: go_dict[pos_class], neg_class: not_k}
    return class_dict

# Checks to make sure my function divides genes into two clasees correctly,
# by checking to see if, after division, the number of unique genes is the
# same as the original
membrane = get_classes(dict_GO, 'membrane')
total_unique_genes = set()
for i in dict_GO.values():
    total_unique_genes = total_unique_genes | i
len(total_unique_genes)  # 9537 total genes original GO dict
# 9537 total genes after dividing into 2 classes
sum([len(i) for i in membrane.values()])
# Does same check as above
list_classes = []
for one_key in dict_GO:
    one = get_classes(dict_GO, one_key)
    a_total = sum([len(i) for i in one.values()])
    if len(total_unique_genes) == a_total:
        list_classes.append(one)
    else:
        raise ValueError('not equal')

##############################################################################
# Reads in processed ml data file, and splits it into different data files,
# eith each file divided into two classes, one class with the GO term, and
# and one without
data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
for classes in list_classes:
    first, second = classes.keys()
    first_t = first.replace(' ', '_')
    data.loc[data.index.isin(classes[first]), 'AraCyc annotation'] = first
    data.loc[data.index.isin(classes[second]), 'AraCyc annotation'] = second
    small = data.dropna(subset=['AraCyc annotation'])
    # No nan here
    # small.isna().sum().sum()
    # Need to edit this as theres spaces in file names
    small.to_csv(first_t + '_GO.txt', sep='\t')
    data['AraCyc annotation'] = np.nan


