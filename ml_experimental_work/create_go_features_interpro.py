# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

Takes all GO terms obtained from Interproscan, and uses them as 
features, does 1HE.
All labels will have values of either 0 or 1, depending if the gene
has that label or not.

Remove features if only 1 gene has it
"""

import pandas as pd

PATH = 'D:/GoogleDrive/machine_learning/my_features/interpro_files/'
FILE = PATH + 'ath_aa_processed.fa.tsv'
OUTPUT = 'go_features_interpro.txt'

lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']
df = pd.read_csv(FILE, sep='\t',  names=lst_names)

lst_selection = ['Protein_Accession', 'GO_annotations']
df_selection = df.loc[:, lst_selection]

df_GOs = df_selection.loc[~df_selection['GO_annotations'].isna(), :]
# Drop duplicates here to reduce df size
df_GOs = df_GOs.drop_duplicates()
df_GOs['split_GOs'] = df_GOs['GO_annotations'].str.split('|')
dropped_df = df_GOs.drop(columns=['GO_annotations'])
exploded_df = dropped_df.explode('split_GOs')
exploded_df = exploded_df.set_index('Protein_Accession')
binary_labels = pd.get_dummies(exploded_df, prefix='go')
combined_rows = binary_labels.groupby(binary_labels.index).sum()

# Drop columns if only 1 gene has that feature
threshold = len(combined_rows) - 1
to_drop = combined_rows.columns[(combined_rows == 0).sum() == threshold]
removed = combined_rows.drop(columns=to_drop)
'''
# Shows number of genes and features
removed.shape
Out[65]: (17231, 1679)
# Checks that all GO features are present in >1 gene
(removed.sum() > 1).all()
Out[37]: True
'''

removed.index.name = 'Gene'
removed.to_csv(OUTPUT, sep='\t')
