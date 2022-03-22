# -*- coding: utf-8 -*-
"""
Created on 100121

@author: weixiong

Creates cis element features for Arabidopsis. Count number of cis element
names and families, per gene

Remove features if only 1 gene has it
"""

import pandas as pd
import numpy as np

# Constants and input variable
FILE ='./AtcisDB/BindingSite.tbl'  # test file: test_cis.tbl
OUTPUT = 'cis_features.txt'

lst_names = ['BS_Id', 'BS_Name', 'Chromosome', 'Strand', 'BS_Genome_Start',
             'BS_Genome_End', 'Promoter_Id', 'BS_Seq', 'BS_Color', 'BS_Family',
             'BS_Motif']
df = pd.read_csv(FILE, sep='\t',  names=lst_names)

lst_selection = ['BS_Name', 'Promoter_Id', 'BS_Family']
df_selection = df.loc[:, lst_selection]

df_selection['Promoter_Id'] = df['Promoter_Id'].str.split('.').str[0]
df_selection['Promoter_Id'] = df_selection['Promoter_Id'].str.upper()
df_selection['BS_Family'].replace('none', np.nan, inplace=True)

dummies = pd.get_dummies(df_selection, columns=['BS_Name', 'BS_Family'], prefix=['cin', 'cif'])
cis_elements = dummies.groupby('Promoter_Id').sum()

cis_elements.index.name = 'Gene'

# Drop columns if only 1 gene has that feature
threshold = len(cis_elements) - 1
to_drop = cis_elements.columns[(cis_elements == 0).sum() == threshold]
'''
# Just to check, no empty columns with no 1s
((cis_elements == 0).sum() > threshold).any()
Out[157]: False
'''
# Just for exploration, see comments below
cin_test = removed[removed.columns[removed.columns.str.startswith('cin_')]]
cif_test = removed[removed.columns[removed.columns.str.startswith('cif_')]]

removed = cis_elements.drop(columns=to_drop)
removed.to_csv(OUTPUT, sep='\t')

'''
# Number of genes and features for cis element names and families
(cin_test.sum(axis=1) == 0).any()
Out[215]: False
cin_test.shape
Out[216]: (25191, 82)

(cif_test.sum(axis=1) == 0).any()
Out[218]: True
cif_test.shape
Out[221]: (25191, 15)
len(cif_test) - sum((cif_test.sum(axis=1) == 0))
Out[223]: 24682
'''
'''
cin_test
Out[4]: 
           cin_ABFs binding site motif  ...  cin_octamer promoter motif
Gene                                    ...                            
AT1G01010                            0  ...                           0
AT1G01020                            0  ...                           0
AT1G01030                            0  ...                           0
AT1G01040                            0  ...                           0
AT1G01050                            0  ...                           0
                               ...  ...                         ...
AT5G67590                            0  ...                           0
AT5G67600                            0  ...                           0
AT5G67610                            0  ...                           0
AT5G67620                            0  ...                           0
AT5G67630                            0  ...                           0

[25191 rows x 82 columns]

cif_test
Out[5]: 
           cif_ABI3VP1  cif_AP2-EREBP  ...  cif_WRKY  cif_bZIP
Gene                                   ...                    
AT1G01010           11              0  ...         8         8
AT1G01020            3              0  ...         0         0
AT1G01030            8              0  ...         2         4
AT1G01040            5              0  ...         3         1
AT1G01050            1              0  ...         0         2
               ...            ...  ...       ...       ...
AT5G67590            4              0  ...         0         1
AT5G67600           11              0  ...         2         3
AT5G67610            9              0  ...         6         4
AT5G67620            5              0  ...         2         4
AT5G67630            0              0  ...         0         0

[25191 rows x 15 columns]

cin_test.max()
Out[6]: 
cin_ABFs binding site motif          3
cin_ABRE binding site motif          3
cin_ABRE-like binding site motif    10
cin_ACE promoter motif               2
cin_AG BS in AP3                     1
                                    ..
cin_TGA1 binding site motif          3
cin_VOZ binding site                 4
cin_W-box promoter motif            34
cin_Z-box promoter motif             4
cin_octamer promoter motif           3
Length: 82, dtype: uint8

cif_test.max()
Out[7]: 
cif_ABI3VP1         142
cif_AP2-EREBP         4
cif_ARF              14
cif_BHLH             15
cif_E2F-DP           18
cif_HB               13
cif_HSF               8
cif_Homeobox         16
cif_LFY              48
cif_MADS             12
cif_MYB              84
cif_MYB-related      10
cif_VOZ PROTEINS      4
cif_WRKY             34
cif_bZIP             75
dtype: uint8
'''
