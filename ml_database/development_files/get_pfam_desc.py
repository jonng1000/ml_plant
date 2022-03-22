# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 21:05:55 2022

@author: weixiong001

Create pfam description file
"""

import pandas as pd

FILE = 'G:/My Drive/machine_learning/my_features/interpro_files/ath_aa_processed.fa.tsv'
OUTPUT = 'pfam_desc.txt'

lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']

df = pd.read_csv(FILE, sep='\t', names=lst_names)


selected = df.loc[df['Analysis'] == 'Pfam', ['Analysis', 'Signature Accession', 'Signature Description']]
pfam = selected.drop_duplicates()
pfam = pfam.reset_index(drop=True)
pfam.index.name = 'id'

pfam.to_csv(OUTPUT, sep='\t')