# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the inteproscan output file, selects the protein domain
information, and counts the number of protein domains per protein).
Also counts the number of protein domains (including and
excluding repeated ones - 2 different features), disordered
regions and transmembrane helixes.

Using Signature accession
instead of description as ID, and represents missing
values as nan.

Modified from analyse_interpro_v4.py in
D:\GoogleDrive\machine_learning\my_features\data_creation_v3
Change from OHE protein domains to counting them, and removing domains which
only appear in 1 protein, from all features
"""

import pandas as pd
#import modin.pandas as pd

# Comment out one of it depending on OS I am using
PATH = 'D:/GoogleDrive/machine_learning/my_features/interpro_files/'
#PATH = '/mnt/d/GoogleDrive/machine_learning/my_features/interpro_files/'

FILE = PATH + 'ath_aa_processed.fa.tsv'
OUTPUT = 'edited_Ath_protein_doms.txt'

lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']
df = pd.read_csv(FILE, sep='\t',  names=lst_names)

lst_selection = ['Protein_Accession', 'Analysis', 'Signature Accession']
df_selection = df.loc[:, lst_selection]
pfam = df_selection.loc[df_selection['Analysis'] == 'Pfam',:]

# Identifies those domains which occur in >1 protein in my data
pfam_nodup = pfam.drop_duplicates()
dummies_nodup = pd.get_dummies(pfam_nodup, columns=['Signature Accession'], prefix=['pfa'])
dummies_nodup.drop(columns=['Analysis'], inplace=True)
temp_domains = dummies_nodup.groupby('Protein_Accession').sum()
temp_filtered = temp_domains.loc[:, temp_domains.sum() > 1]

# Counting number of each domain per protein, and remove domains if it only
# appears once in all the proteins
dummies = pd.get_dummies(pfam, columns=['Signature Accession'], prefix=['pfa'])
dummies.drop(columns=['Analysis'], inplace=True)
pfam_domains = dummies.groupby('Protein_Accession').sum()
pfam_filtered = pfam_domains.loc[:,temp_filtered.columns]

'''
# Seeing the range of pfam domain counts
pfam_filtered.values.reshape(-1).sort()
test = pfam_filtered.values.reshape(-1)
test.sort()
test
Out[63]: array([ 0,  0,  0, ..., 23, 30, 32], dtype=uint8)
'''

# Counts number of domains, including repeated ones
pfam_counts = pfam_filtered.sum(axis=1)
pfam_counts.name = 'num_counts'

# Counts number of domains, excluding repeated ones
pfam_nodup = pfam.drop_duplicates()
grouped_pfam = pfam_nodup.groupby('Protein_Accession')
pfam_u_counts = grouped_pfam.count().loc[:, 'Signature Accession']
pfam_u_counts.name = 'num_u_counts'

# Counts mobi database hits
mobi = df_selection.loc[df_selection['Analysis'] == 'MobiDBLite',:]
mobi_grp = mobi.groupby(['Protein_Accession']).count()
mobi_counts = mobi_grp.loc[:, 'Signature Accession']
mobi_counts.name = 'mob_counts'

# Counts tmhmm database hits
tmhmm = df_selection.loc[df_selection['Analysis'] == 'TMHMM',:]
tmhmm_grp = tmhmm.groupby(['Protein_Accession']).count()
tmhmm_counts = tmhmm_grp.loc[:, 'Signature Accession']
tmhmm_counts.name = 'tmh_counts'

pro_dom = pd.concat([pfam_filtered, pfam_counts, pfam_u_counts, mobi_counts,
                     tmhmm_counts], axis=1)
pro_dom.index.name = 'Gene'
pro_dom.to_csv(OUTPUT, sep='\t')

# Extra info just for checking
# Number of GB used in memory by dataframe
#>>> sum(pro_dom.memory_usage())/1000/1000/1000
#0.572775696
# About 71 M cells in dataframe
#>>> pro_dom.size
#71571591
# Dimensons of dataframe
#>>> pro_dom.shape
#(25371, 2821)
# Calculates the number of 0s and 1s in dataframe
# Not entirely accurate as some of the 1s are from non-domain features,
# but the general idea, that domains form a sparse matrix, still holds
#>>> pro_dom.isin([0]).sum().sum()
#61488572
#>>> pro_dom.isin([1]).sum().sum()
#61043

'''
pro_dom.max().sort_values()
Out[94]: 
pfa_PF04483     1.0
pfa_PF05278     1.0
pfa_PF05285     1.0
pfa_PF05327     1.0
pfa_PF14306     1.0

pfa_PF01422    12.0
pfa_PF04554    32.0
num_counts     32.0
tmh_counts     37.0
mob_counts     58.0
Length: 2765, dtype: float64
'''