# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the inteproscan output file, selects the protein domain
information, appends a unique prefix to such information depending on which
database it comes from, and converts it into dummary variables (binary features)
Total estimated time to run this is 15 min, as converting the protein domains to
binary features takes 12 min
"""

import pandas as pd

FILE = "interpro_files/ath_aa_processed.fa.tsv"
OUTPUT = "protein_doms.txt"

# Column names in interpro results file
lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']
# Prefix dictionary to append protein database names to protein
# domain names
prefix_dict = {'Pfam': 'pfa_', 'ProSiteProfiles': 'psprof_', 'CDD': 'cdd_',
               'MobiDBLite': 'mob_', 'TMHMM': 'tmh_', 'ProSitePatterns': 'pspat_',
               'PRINTS': 'pri_', 'TIGRFAM': 'tig_', 'Hamap': 'ham_',
               'SFLD': 'sfl_', 'SMART': 'sma_'}

df = pd.read_csv(FILE, sep='\t',  names=lst_names)

lst_selection = ['Protein_Accession', 'Sequence Length',
                 'Analysis', 'Signature Accession', 'Signature Description',]
# Simplifies df
df_selection = df.loc[:, lst_selection]
# Remove rows where there's no protein domain desc
p_dom_info = df_selection.dropna(subset=['Signature Description'])
# Remove rows where there's duplicate protein domains
# This occurs as mutliple domains can occur along the aa length
# Used copy() as this prevents SettingWithCopyWarning in the below replacement
# operations
no_dup_pdom = p_dom_info.drop_duplicates().copy()
temp = no_dup_pdom.loc[:, 'Analysis'].replace(prefix_dict)
no_dup_pdom.loc[:, 'Analysis'] = temp
no_dup_pdom.loc[:, 'Signature Description'] = no_dup_pdom['Analysis'] +\
                                              no_dup_pdom['Signature Description']
# This is needed to SettingWithCopyWarning error, which occurs even when I
# use .loc on both sides of the = sign when replacing values, dunno why
# Note: .copy() used above, may remove the need for copy() below, can test it
# out in future versions of this code
copy_ndpd = no_dup_pdom.copy()
temp = no_dup_pdom.loc[:, 'Signature Description'].str.replace(' ','_')
temp = temp.str.replace("'",'')
temp = temp.str.replace('\.','')
copy_ndpd.loc[:, 'Signature Description'] = temp


concat_str =  copy_ndpd.groupby(['Protein_Accession'])['Signature Description'].\
              apply(' '.join)
#len(concat_str) #  Gives 25639, hence it tallies with the original number
#of genes before data processing above
# 12 min for this one hot encoding step
dummies = concat_str.str.get_dummies(sep=' ')
dummies.to_csv(OUTPUT, sep='\t')

# Extra info just for checking
# Number of GB used in memory by dataframe
#>>> sum(dummies.memory_usage())/1000/1000/1000
#1.990486896
# About 248 M cells in dataframe
#>>> dummies.size
#248621383
# No NA values
#>>> dummies.isnull().values.any()
#False
# Calculates the number of 0s and 1s in dataframe
#>>> dummies.isin([0]).sum().sum()
#248531839
#>>> dummies.isin([1]).sum().sum()
#89544
# % of 1s in dataframe, matrix is very sparse
#>>> (prot_dom_bins.isin([1]).sum().sum()/prot_dom_bins.size) * 100
#0.036016210238843376
