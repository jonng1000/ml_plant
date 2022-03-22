# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:51:45 2021

@author: weixiong001

Get raw features from TF and TG datasets from paper's supplementary info,
renames them, and combines to form one dataset of features for ml.
"""

import pandas as pd

FILE = 'feature_name_map.txt'
FILE2 = 'tf_raw_features.txt'
FILE3 = 'tg_raw_features.txt'
OUTPUT = 'tt_coexp_features.txt'

map_df = pd.read_csv(FILE, sep='\t')
tf_df = pd.read_csv(FILE2, sep='\t', index_col=0)
tg_df = pd.read_csv(FILE3, sep='\t', index_col=0)

selector = map_df['ID']

tf_selection = set(selector).intersection(set(tf_df.columns))
tf_selected_df = tf_df.loc[:, tf_selection]
tg_selection = set(selector).intersection(set(tg_df.columns))
tg_selected_df = tg_df.loc[:, tg_selection]

mapping_dict = map_df.set_index('ID')['New Desc'].to_dict()
renamed_tf = tf_selected_df.rename(columns=mapping_dict)
renamed_tg = tg_selected_df.rename(columns=mapping_dict)

'''
# Duplicate tf genes in tg genes set
# 291 duplicates
duplicate = set(renamed_tf.index).intersection(renamed_tg.index)
# All tf genes are in tg data set, so just use this
renamed_tf.drop(index=list(duplicate))
Out[30]: 
Empty DataFrame
'''
renamed_tg.index.name = 'Gene'
renamed = renamed_tg.rename(columns=lambda x: 'ttf_'+x)
renamed.to_csv(OUTPUT, sep='\t')

'''
# Altho these feature are continuous, wanted to check that features have >1 gene
# All features have this
threshold = len(renamed) - 1
# No entries here
to_drop = renamed.columns[(renamed == 0).sum() == threshold]

renamed
Out[57]: 
           ttf_Percentage of CC in promoter sequence of TG  ...  ttf_Number of differentially methylated CHH in promoter of TG (Kawakatsu et al., 2016)
Gene                                                        ...                                                                                        
AT1G01010                                         0.039039  ...                                                  1                                     
AT1G01030                                         0.021021  ...                                                  0                                     
AT1G01040                                         0.027027  ...                                                  1                                     
AT1G01050                                         0.030030  ...                                                  0                                     
AT1G01060                                         0.032032  ...                                                  0                                     
                                                   ...  ...                                                ...                                     
AT5G67560                                         0.037037  ...                                                  0                                     
AT5G67580                                         0.029029  ...                                                  0                                     
AT5G67590                                         0.026026  ...                                                  0                                     
AT5G67600                                         0.035035  ...                                                  0                                     
AT5G67630                                         0.049049  ...                                                  1                                     

[15879 rows x 76 columns]

renamed.max()
Out[58]: 
ttf_Percentage of CC in promoter sequence of TG                                                  0.110110
ttf_Percentage of CT in promoter sequence of TG                                                  0.125125
ttf_Percentage of GG in promoter sequence of TG                                                  0.134134
ttf_Maximal length of 5'UTR of all isoforms                                                   3208.000000
ttf_Minimal length of 5'UTR of all isoforms                                                   2056.000000
    
ttf_Number of differentially methylated CpG surrounding TSS of TG (Kawakatsu et al., 2016)       1.000000
ttf_Expression of near genes at distance <500bp                                                  7.993270
ttf_Number of differentially methylated CpG surrounding TSS of TG (Schmitz et al., 2013)         1.000000
ttf_Percentage of GC in promoter sequence of TG                                                  0.067067
ttf_Number of differentially methylated CHH in promoter of TG (Kawakatsu et al., 2016)           2.000000
Length: 76, dtype: float64
'''