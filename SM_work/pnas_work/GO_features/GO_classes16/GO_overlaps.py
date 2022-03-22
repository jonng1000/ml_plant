# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

From GO_check.py. First two blocks taken from GO_check.py, subsequent ones are
new additions.
"""
import pandas as pd

GO_SELECT = 'D:/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'
ML_DATA = "fully_processed_edited.txt"
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

mega_lst = [['pos class', 'pos only', 'inter', 'neg only', 'neg class']]
for one in dict_GO.keys():
    pos_class = one
    # pos_class = 'membrane'
    neg_class = 'not ' + pos_class
    gene_set = set()
    for k in dict_GO.keys():
        if k != pos_class:
            gene_set = gene_set | dict_GO[k]
    inter = gene_set & dict_GO[pos_class]
    not_k = gene_set - inter
    k_only = dict_GO[pos_class] - inter
    mega_lst.append(
        [pos_class, len(k_only), len(inter), len(not_k), neg_class]
        )

record = pd.DataFrame.from_records(mega_lst[1:],
                                   columns=mega_lst[0]
                                   )
record.index.name = 'id'
record.to_csv('classes_counts.txt', sep='\t')


