# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the inteproscan output file, selects the protein domain
information, and counts the number of times each database in interpro appears in
the output file.
"""

import pandas as pd

FILE = "interpro_files/ath_aa_processed.fa.tsv"

lst_names = ['Protein_Accession', 'Sequence_MD5_digest', 'Sequence Length',
             'Analysis', 'Signature Accession', 'Signature Description',
             'Start location', 'Stop location', 'Score', 'Status', 'Date',
             'InterPro_annotations_accession',
             'InterPro_annotations_description', 'GO_annotations',
             'Pathways_annotations']

df = pd.read_csv(FILE, sep='\t',  names=lst_names)
'''
>>> df['InterPro_annotations_accession'].nunique()
8776
'''
'''
>>> df[['Protein_Accession', 'InterPro_annotations_accession']].dropna().nunique()
Protein_Accession                 23364
InterPro_annotations_accession     8776
dtype: int64
'''

lst_selection = ['Protein_Accession', 'Sequence Length',
                 'Analysis', 'Signature Accession', 'Signature Description',]
# Simplifies df
df_selection = df.loc[:, lst_selection]
'''
>>> df_selection['Analysis'].value_counts()
PANTHER            53144
Pfam               37910
MobiDBLite         36501
Gene3D             30118
SUPERFAMILY        24462
ProSiteProfiles    22475
TMHMM              21438
PRINTS             19471
SMART              18125
CDD                12558
ProSitePatterns     7203
Coils               6867
TIGRFAM             6007
PIRSF               1723
Hamap                960
SFLD                 450
'''
all_unique_feat = df_selection.loc[:, ['Analysis', 'Signature Accession']].\
                  drop_duplicates()
'''
>>> all_unique_feat.groupby(['Analysis']).count()
                 Signature Accession
Analysis
CDD                             2606
Coils                              1
Gene3D                          1732
Hamap                            506
MobiDBLite                         1
PANTHER                        21320
PIRSF                            560
PRINTS                           437
Pfam                            4149
ProSitePatterns                  679
ProSiteProfiles                  634
SFLD                              68
SMART                            693
SUPERFAMILY                      986
TIGRFAM                          797
TMHMM                              1
'''
all_unique_genes = df_selection.loc[:, ['Protein_Accession', 'Analysis']].\
                  drop_duplicates()
'''
>>> all_unique_genes.groupby(['Analysis']).count()
                 Protein_Accession
Analysis
CDD                           9836
Coils                         4354
Gene3D                       16981
Hamap                          934
MobiDBLite                   11305
PANTHER                      25012
PIRSF                         1519
PRINTS                        3701
Pfam                         21838
ProSitePatterns               5183
ProSiteProfiles              10269
SFLD                           234
SMART                         8726
SUPERFAMILY                  16832
TIGRFAM                       3061
TMHMM                         6901
'''
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
database_counts = copy_ndpd['Analysis'].value_counts()
protein_counts = copy_ndpd['Protein_Accession'].unique()
"""
>>> copy_ndpd['Analysis'].value_counts()
Pfam               31251
ProSiteProfiles    12929
CDD                11855
MobiDBLite         11305
TMHMM               6901
ProSitePatterns     6635
PRINTS              4341
TIGRFAM             3271
Hamap                958
SFLD                 450
SMART                 35
Name: Analysis, dtype: int64
>>> copy_ndpd['Protein_Accession'].unique()
array(['AT4G21230', 'AT3G26880', 'AT5G44170', ..., 'AT5G48560',
       'AT2G03320', 'AT1G08720'], dtype=object)
>>> len(copy_ndpd['Protein_Accession'].unique())
25639
"""
