# -*- coding: utf-8 -*-
"""
Created on 100121

@author: weixiong

Creates twas features for Arabidopsis. Count number of times each phenotype
has been found to be associated with each gene

Drop feature if only 1 gene has it
"""

import pandas as pd
import numpy as np

# Constants
FILE ='twas_edited.txt'
OUTPUT = 'twas_features.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
genes_df = df.set_index('Gene')
'''
# Check that all genes meet the statistical significance threshold of
# p < 0.05 for both pearson and spearman
fdr_p = genes_df['FDR_Pearson'] < 0.05
fdr_p.all()
Out[67]: True
fdr_s = genes_df['FDR_Spearman'] < 0.05
fdr_s.all()
Out[69]: True
'''
genes_pheno = genes_df.loc[:, 'Phenotype ontology']
'''
# Check that all genes have expected names
{i[:4] for i in genes_pheno.index}
Out[73]: {'AT1G', 'AT2G', 'AT3G', 'AT4G', 'AT5G', 'ATCG', 'ATMG'}
'''
'''
# Data has nan
genes_pheno.isnull().all()
Out[77]: False
'''
dropped_na = genes_pheno.dropna()
dummies = pd.get_dummies(dropped_na, prefix='twa')
summed = dummies.groupby('Gene').sum()
'''
# Shows that some genes have >1 counts
np.sort(summed.values.flatten())
Out[96]: array([ 0,  0,  0, ..., 37, 39, 39], dtype=uint8)
'''

# Drop columns if only 1 gene has that feature
threshold = len(summed) - 1
to_drop = summed.columns[(summed == 0).sum() == threshold]
removed = summed.drop(columns=to_drop)
'''
# Ensures no columns are all 0s
((summed == 0).sum() > threshold).any()
Out[180]: False
'''

removed.to_csv(OUTPUT, sep='\t')
'''
removed
Out[188]: 
           twa_arsenic concentration  ...  twa_zinc concentration
Gene                                  ...                        
AT1G01010                          0  ...                       0
AT1G01040                          0  ...                       0
AT1G01046                          0  ...                       0
AT1G01050                          0  ...                       1
AT1G01060                          0  ...                       0
                             ...  ...                     ...
ATMG01360                          0  ...                       0
ATMG01370                          0  ...                       0
ATMG01380                          0  ...                       0
ATMG01390                          0  ...                       0
ATMG01410                          0  ...                       1

[16583 rows x 28 columns]

removed.max()
Out[189]: 
twa_arsenic concentration                         1
twa_boron concentration                           1
twa_cadmium concentration                         1
twa_cauline axillary branch number                1
twa_cobalt concentration                          1
twa_copper concentration                          1
twa_days to flowering trait                      25
twa_fruit set trait                               1
twa_gravity response trait                        1
twa_leaf number                                   2
twa_lodicule morphology trait                     1
twa_magnesium concentration                       1
twa_manganese concentration                       1
twa_molybdenum concentration                      2
twa_nickel concenteration                         1
twa_other miscellaneous trait                    39
twa_phosphorus concentration                      1
twa_plant dry weight                              1
twa_potassium concentration                       1
twa_root branching                                1
twa_seed dormancy                                 1
twa_seed weight                                   2
twa_selenium concentration                        1
twa_shoot system growth and development trait     2
twa_sodium concentration                          2
twa_stomatal process related trait                2
twa_sulfur concentration                          2
twa_zinc concentration                            1
dtype: uint8
'''
