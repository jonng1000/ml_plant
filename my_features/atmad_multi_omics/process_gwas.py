# -*- coding: utf-8 -*-
"""
Created on 100121

@author: weixiong

Creates gwas features for Arabidopsis. Count number of times each phenotype
has been found to be associated with each gene.
Drop feature if only 1 gene has it
"""

import pandas as pd
import numpy as np

# Constants
FILE ='gwas_edited.txt'
OUTPUT = 'gwas_features.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
rem_genes_nan = df.dropna(subset=['Genename'])
only_pheno = rem_genes_nan.loc[:, ['Genename', 'Phenotype ontology']]
genes_df = only_pheno.set_index('Genename')
"""
# Shows the variation in gene names, as not all are genes so they need to be
# removed or changed
{i[:4] for i in genes_df.index}
Out[30]: {'AT1G', 'AT2G', 'AT3G', 'AT4G', 'AT5G', 'Exon', 'Gene'}
"""
rem_exon_names = genes_df.drop(
    index=genes_df.index[genes_df.index.str.startswith('Exon')]
    )
"""
# Shows rows which are not genes which need to be removed
genes_df.index[genes_df.index.str.startswith('Exon')]
Out[32]: 
Index(['Exon_1_20319375_20319554', 'Exon_1_16628310_16628661',
       'Exon_3_7372760_7374364', 'Exon_3_7372760_7374364',
       'Exon_3_7372760_7374364', 'Exon_1_16628310_16628661',
       'Exon_1_16401870_16402916', 'Exon_2_6770784_6772235',
       'Exon_1_16666418_16666662', 'Exon_2_6770784_6772235',
       ...
       'Exon_3_12294053_12294137', 'Exon_2_4773143_4773245',
       'Exon_1_2415041_2415970', 'Exon_1_15637605_15637668',
       'Exon_1_13372521_13372661', 'Exon_1_13372521_13372661',
       'Exon_1_13372521_13372661', 'Exon_1_13372521_13372661',
       'Exon_1_13372521_13372661', 'Exon_1_13372521_13372661'],
      dtype='object', name='Genename', length=1307)
"""
names_mod = rem_exon_names.index[rem_exon_names.index.str.startswith('Gene')]
dict_rename = {i:i[5:] for i in names_mod}
renamed = rem_exon_names.rename(index=dict_rename)
dummies = pd.get_dummies(renamed, prefix=['gwa'])
summed = dummies.groupby('Genename').sum()
# Drop columns if only 1 gene has that feature
threshold = len(summed) - 1
to_drop = summed.columns[(summed == 0).sum() == threshold]
'''
# Just to check, no empty columns with no 1s
((summed == 0).sum() > threshold).any()
Out[157]: False
'''
removed = summed.drop(columns=to_drop)
removed.to_csv(OUTPUT, sep='\t')
'''
removed
Out[171]: 
           gwa_DSDS50  ...  gwa_zinc concentration
Genename               ...                        
AT1G01160           0  ...                       0
AT1G01170           0  ...                       0
AT1G01180           0  ...                       0
AT1G01240           0  ...                       0
AT1G01630           0  ...                       0
              ...  ...                     ...
AT5G67580           0  ...                       0
AT5G67590           0  ...                       0
AT5G67610           0  ...                       0
AT5G67620           0  ...                       0
AT5G67640           0  ...                       0

[8165 rows x 33 columns]

removed.max()
Out[172]: 
gwa_DSDS50                                        36
gwa_anthocyanin content                            1
gwa_arsenic concentration                         16
gwa_bacterial disease resistance                  84
gwa_cadmium concentration                         11
gwa_cobalt concentration                          12
gwa_days to flowering trait                       28
gwa_days to germinate                              3
gwa_flowering time trait                           4
gwa_germinability in dark                         18
gwa_hybrid incompatibility                         4
gwa_lateral root length                           36
gwa_lateral root number                            2
gwa_leaf chlorosis                                21
gwa_leaf necrosis                                 25
gwa_leaf number                                   10
gwa_metabolite content trait                     191
gwa_molybdenum concentration                      38
gwa_other miscellaneous trait                    235
gwa_plant dry weight                               4
gwa_protist disease resistance                     1
gwa_relative root length                          34
gwa_reproductive growth time                       2
gwa_rolled leaf                                    4
gwa_root branching                                 4
gwa_root mass density                             26
gwa_root morphology trait                         36
gwa_seed dormancy                                131
gwa_seed weight                                    1
gwa_shoot system growth and development trait     22
gwa_sodium concentration                          22
gwa_yield trait                                   18
gwa_zinc concentration                             3
dtype: uint8
'''

