# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

Takes all GO terms, and uses them as features, does 1HE
All labels will have values of either 0 or 1, depending if the gene
has that label or not

Modified from all_labels_ml.py in 
D:\GoogleDrive\machine_learning\my_features\ml_runs_v2

Takes ~1 min to run

Remove features if only 1 gene has it
"""
import pandas as pd

GO_TERMS = 'D:/GoogleDrive/machine_learning/GO_labels/sort_GO_gene_counts.txt'
GO_FEAT = 'go_dataset.txt'

go_terms_df = pd.read_csv(GO_TERMS, sep='\t', index_col=0)

# Get all go terms and convert them into binary values, to indicate
# if the gene has that label or not
go_terms_df.loc[:, ['Genes']] = go_terms_df['Genes'].str.split(' ')
one_gene_cp = go_terms_df.explode('Genes').loc[:, ['Genes']]
one_gene_cp = one_gene_cp.reset_index()
one_gene_cp = one_gene_cp.set_index('Genes')
binary_labels = pd.get_dummies(one_gene_cp, prefix='go')
# These combine duplicated genes into the same row, as the same
# gene occuplies multiple rows if it has >1 go term
# After combining duplicates, each row has one gene, with all its
# labels
combined_rows = binary_labels.groupby(binary_labels.index).sum()

# Drop columns if only 1 gene has that feature
threshold = len(combined_rows) - 1
# About 1.5k GO terms have only 1 gene
to_drop = combined_rows.columns[(combined_rows == 0).sum() == threshold]
removed = combined_rows.drop(columns=to_drop)

'''
# Shows number of genes and features
removed.shape
Out[65]: (14374, 3645)

removed
Out[24]: 
       go_GO:0000002  go_GO:0000003  ...  go_GO:2001280  go_GO:2001289
Genes                                ...                              
AAN                0              0  ...              0              0
AAR1               0              0  ...              0              0
AAR2               0              0  ...              0              0
ACL1               0              0  ...              0              0
ACL2               0              0  ...              0              0
             ...            ...  ...            ...            ...
XRS11              0              0  ...              0              0
XRS4               0              0  ...              0              0
XRS9               0              0  ...              0              0
XTC1               0              0  ...              0              0
XTC2               0              0  ...              0              0

[14374 rows x 3645 columns]
removed.sum()
Out[26]: 
go_GO:0000002      4
go_GO:0000003     16
go_GO:0000009      2
go_GO:0000014      5
go_GO:0000023      4

go_GO:2001141    521
go_GO:2001147      2
go_GO:2001227      2
go_GO:2001280      2
go_GO:2001289      5
Length: 3645, dtype: int64
'''
removed.to_csv(GO_FEAT, sep='\t')