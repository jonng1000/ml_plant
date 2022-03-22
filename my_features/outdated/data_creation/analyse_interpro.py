# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the inteproscan output file, selects the protein domain
information, and converts it into dummary variables (binary features)
Total estimated time to run this is 15 min, as converting the protein domains to
binary features takes 12 min
"""

import pandas as pd

FILE = "ath_aa_processed.fa.tsv"
OUTPUT = "protein_doms.txt"

lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']

df = pd.read_csv(FILE, sep='\t',  names=lst_names)

lst_selection = ['Protein_Accession', 'Sequence Length',
                 'Analysis', 'Signature Accession', 'Signature Description',]
# Simplifies df
df_selection = df.loc[:, lst_selection]
# Remove rows where there's no protein domain desc
p_dom_info = df_selection.dropna(subset=['Signature Description'])
# Remove rows where there's duplicate protein domains
# This occurs as mutliple domains can occur along the aa length
no_dup_pdom = p_dom_info.drop_duplicates()
# This is needed to SettingWithCopyWarning error, which occurs even when I
# use .loc on both sides of the = sign when replacing values, dunno why
copy_ndpd = no_dup_pdom.copy()
copy_ndpd.loc[:, 'Signature Description'] = \
no_dup_pdom.loc[:, 'Signature Description'].str.replace(' ','_')
temp = copy_ndpd.copy()
temp.loc[:, 'Signature Description'] = \
copy_ndpd.loc[:, 'Signature Description'].str.replace("'",'')
copy_ndpd = temp

grouped_prot = copy_ndpd.groupby('Protein_Accession')
#concat_pdesc = grouped_prot['Signature Description'].\
#               transform(lambda x: ' '.join(x))
concat_str = grouped_prot.transform(lambda x: ' '.join(x))

copy_ndpd.loc[:, ['Analysis', 'Signature Accession', 'Signature Description']] = concat_str[['Analysis', 'Signature Accession', 'Signature Description']]
#copy_ndpd.loc[:, 'Signature Description'] = concat_pdesc
unique_genes = copy_ndpd.drop_duplicates()
#len(set(no_dup_pdom['Protein_Accession'])) #  Gives 25639
# unique_genes has 25639 rows, hence it tallies with the original number of genes
# before data processing above
pdesc = unique_genes.loc[:, ['Protein_Accession', 'Signature Description']]
# 12 min for this step
# Protein domains are tagged with PD for easy reference in future
dummies = pdesc.loc[:, 'Signature Description'].str.get_dummies(sep=' ').\
          add_prefix('PD_')
#pdesc.loc[:, 'Protein_Accession']
combined_extras = pd.concat([pdesc, dummies], axis=1).\
                  drop(columns=['Signature Description'])
prot_dom_bins = combined_extras.set_index('Protein_Accession')
prot_dom_bins.to_csv(OUTPUT, sep='\t')

# Extra info just for checking
# Number of GB used in memory by dataframe
#>>> sum(prot_dom_bins.memory_usage())/1000/1000/1000
#1.986919944
# About 248 M cells in dataframe
#>>> prot_dom_bins.size
#248339354
# No NA values
#>>> prot_dom_bins.isnull().values.any()
#False
# Calculates the number of 0s and 1s in dataframe
#>>> prot_dom_bins.isin([0]).sum().sum()
#248249841
#>>> prot_dom_bins.isin([1]).sum().sum()
#89513
# % of 1s in dataframe, matrix is very sparse
#>>> (prot_dom_bins.isin([1]).sum().sum()/prot_dom_bins.size) * 100
#0.03604462947906356
