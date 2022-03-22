# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 20:39:19 2021

@author: weixiong001
"""
import pandas as pd
import numpy as np

FILE = "Supplemental_Data_set_3_modified.txt"
OUTPUT = 'lloyd_features.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

'''
# About 27k genes
df.shape
Out[33]: (27206, 13)
# Most Ka/Ks - O. sativa values are missing
len(df['Ka/Ks - O. sativa'][df['Ka/Ks - O. sativa'] != '?'])
Out[32]: 5339
# Less than half of Ka/Ks - V. vinifera are missing
len(df['Ka/Ks - V. vinifera'][df['Ka/Ks - V. vinifera'] != '?'])
Out[34]: 15940
# Less than half of Ka/Ks - A. lyrata are missing
len(df['Ka/Ks - A. lyrata'][df['Ka/Ks - A. lyrata'] != '?'])
Out[35]: 17180
# Less than half of Ka/Ks - P. trichocarpa are missing
len(df['Ka/Ks - P. trichocarpa'][df['Ka/Ks - P. trichocarpa'] != '?'])
Out[37]: 17807
# Most Ka/Ks - P. patens values are missing
len(df['Ka/Ks - P. patens'][df['Ka/Ks - P. patens'] != '?'])
Out[38]: 4798

# Rejected features: Ka/Ks - O. sativa, Ka/Ks - P. patens
'''
'''
# Majority of these features is present
len(df['Ks with putative paralog'][df['Ks with putative paralog'] != '?'])
Out[39]: 18165
len(df['Ka/Ks with putative paralog'][df['Ka/Ks with putative paralog'] != '?'])
Out[40]: 18148

# Accept all features
'''
'''
# Majority of these features is present
len(df['Sequence conservation in Fungi (% ID)'][df['Sequence conservation in Fungi (% ID)'] != '?'])
Out[41]: 27206
len(df['Sequence conservation in Metazoans (% ID)'][df['Sequence conservation in Metazoans (% ID)'] != '?'])
Out[42]: 27206
len(df['Sequence conservation in plants (% ID)'][df['Sequence conservation in plants (% ID)'] != '?'])
Out[44]: 27206

# Accept all features
'''
'''
# Majority of these features is present
len(df['Nucleotide diversity'][df['Nucleotide diversity'] != '?'])
Out[45]: 26512
len(df['Percent identity with putative paralog'][df['Percent identity with putative paralog'] != '?'])
Out[46]: 23074
len(df['Gene body methylated'][df['Gene body methylated'] != '?'])
Out[47]: 23491

# Accept all features
'''

replace = df.replace('?', np.nan)
convert_float = replace.astype('float64')
dropped = convert_float.drop(columns=['Ka/Ks - O. sativa', 'Ka/Ks - P. patens'])
dropped = dropped.loc[:, ['Ka/Ks - V. vinifera', 'Ka/Ks - A. lyrata',
                          'Ka/Ks - P. trichocarpa',
                          'Ka/Ks with putative paralog',
                          'Ks with putative paralog',
                          'Percent identity with putative paralog',
                          'Sequence conservation in Fungi (% ID)',
                          'Sequence conservation in Metazoans (% ID)',
                          'Sequence conservation in plants (% ID)',
                          'Nucleotide diversity', 'Gene body methylated']
                      ]
renamed = dropped.rename(columns={'Ka/Ks - V. vinifera': 'con_dNdS - V. vinifera',
                                  'Ka/Ks - A. lyrata': 'con_dNdS - A. lyrata',
                                  'Ka/Ks - P. trichocarpa': 'con_dNdS - P. trichocarpa',
                                  'Ka/Ks with putative paralog': 'con_dNdS with putative paralog',
                                  'Ks with putative paralog': 'con_dS with putative paralog',
                                  'Percent identity with putative paralog': 'con_Percent identity with putative paralog',
                                  'Sequence conservation in Fungi (% ID)': 'con_Sequence conservation in Fungi (% ID)',
                                  'Sequence conservation in Metazoans (% ID)': 'con_Sequence conservation in Metazoans (% ID)',
                                  'Sequence conservation in plants (% ID)': 'con_Sequence conservation in plants (% ID)',
                                  'Nucleotide diversity': 'ntd_Nucleotide diversity',
                                  'Gene body methylated': 'gbm_Gene body methylated'
                                  })

renamed.to_csv(OUTPUT, sep='\t')

'''
renamed.loc[:, renamed.columns.str.startswith('con_')]
Out[34]: 
              con_dNdS - V. vinifera  ...  con_Sequence conservation in plants (% ID)
Locus number                          ...                                            
AT1G01010                        NaN  ...                                       40.61
AT1G01020                   0.227884  ...                                       50.90
AT1G01030                        NaN  ...                                       74.55
AT1G01040                   0.099502  ...                                       74.18
AT1G01050                        NaN  ...                                       87.94
                             ...  ...                                         ...
AT5G67600                        NaN  ...                                        0.00
AT5G67610                        NaN  ...                                       48.39
AT5G67620                        NaN  ...                                       73.63
AT5G67630                        NaN  ...                                       87.58
AT5G67640                        NaN  ...                                       37.25

[27206 rows x 9 columns]
renamed.loc[:, ~renamed.columns.str.startswith('con_')]
Out[35]: 
              ntd_Nucleotide diversity  gbm_Gene body methylated
Locus number                                                    
AT1G01010                     0.000532                       0.0
AT1G01020                     0.002612                       0.0
AT1G01030                     0.001129                       0.0
AT1G01040                     0.000677                       1.0
AT1G01050                     0.000134                       0.0
                               ...                       ...
AT5G67600                     0.000115                       0.0
AT5G67610                     0.002524                       0.0
AT5G67620                     0.002252                       0.0
AT5G67630                     0.001480                       0.0
AT5G67640                     0.003134                       0.0

[27206 rows x 2 columns]

renamed.loc[:, ~renamed.columns.str.startswith('con_')].sum()
Out[36]: 
ntd_Nucleotide diversity     112.30066
gbm_Gene body methylated    4350.00000
dtype: float64
'''