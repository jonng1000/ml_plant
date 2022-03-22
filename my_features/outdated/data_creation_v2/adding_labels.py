# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

With a class label specified, adds a column with the class labels and splits
genes into positive and negative classes. Positive class is the genes with the
class label, and negative class is the genes with all other labels. Remove
overlaps in negative class, so all genes with class and other labels, are
considered to be in the positive class, and taken out from the negative class.
Remove genes which don't belong to both positive and negative classes and
saves the smaller, resulting dataframe.
"""
import pandas as pd
import numpy as np

GO_SELECT = '/mnt/d/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'
ML_DATA = 'combined_data.txt'
# Used to add to file name
CLASS_LABEL = 'Golgi_apparatus'

colnames=['GO class', 'number', 'GO cat', 'GO name', 'genes'] 
selection = pd.read_csv(GO_SELECT, sep="\t", names=colnames, header=None)
# GO terms in GO file uses space instead of _
# This will also be used to fill in values in dataframe when required
class_name = CLASS_LABEL.replace('_', ' ')
not_in_class = 'not ' + class_name

one_class = selection.loc[selection['GO name'] == class_name, :]
# Hardcode index since this is only supposed to have one item in series
lst_genes = one_class['genes'].iloc[0].split()
set_genes = set(lst_genes)
# Checks that there are no duplicate genes in list of gene names
# No duplicates expected as I'm looking at only 1 class
print('No duplicates in', class_name,  'class:', len(lst_genes) == len(set_genes))
total_genes = selection['number'].sum()
print('Total genes in all selected GO classes with experimental evidence:',
      total_genes)

other_classes = selection.loc[selection['GO name'] != class_name, :]
lst_other_genes = other_classes['genes'].str.cat(sep=' ').split()
set_other_genes = set(lst_other_genes)
# Checks that there are no duplicate genes in list of gene names
# Can have duplicates as many classes are examined here, and genes can be in
# >1 class
print('No duplicates in other classe:',
      len(lst_other_genes) == len(set_other_genes))

inter = set_genes & set_other_genes
set_only_others = set_other_genes - inter
print(len(set_genes), 'genes found in the', CLASS_LABEL, 'class')
print(len(set_other_genes), 'genes found in other classes')
print(len(inter), 'genes overlap between',  CLASS_LABEL, 'and other classes')
print(len(set_only_others), 'genes exclusively found in other classes')

data = pd.read_csv(ML_DATA, sep='\t', index_col=0)
# positive class: class_name, negative class: not_in_class
data['class_label'] = np.nan
data.loc[data.index.isin(set_genes), 'class_label'] = class_name
data.loc[data.index.isin(set_only_others), 'class_label'] = not_in_class
small = data.dropna(subset=['class_label'])
'''
# No nan in class_label column
>>> small['class_label'].value_counts(dropna=False)
not Golgi apparatus    8843
Golgi apparatus         675
Name: class_label, dtype: int64
'''
small.to_csv(CLASS_LABEL + '_GO.txt', sep='\t')
