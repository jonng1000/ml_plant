# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 15:30:33 2021

@author: weixiong001

Calculate original proportion of feature categories in clusters
"""

import pandas as pd


FILE = 'feat_cat_info.txt'
OUTPUT = 'categories_orig_prop.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)

cat_counts = df.groupby(['feat_cluster_id', 'feat_category']).size()\
    .unstack(fill_value=0)
cat_counts.columns.name = None

# 39 feature categories in total
all_cats = ['GO_biological_process', 'GO_cellular_component', 'GO_molecular_function',
            'DGE_general molecular function', 'DGE_growth and development',
            'DGE_infection and immunity', 'DGE_light and circadian', 'DGE_stress and stimulus',
            'PPI clusters', 'Aranet clusters', 'Coexp clusters', 'Regulatory clusters',
            'Homolog features', 'Diurnal timepoints', 'Single copy', 'Tandemly duplicated',
            'Gene body methlyated', 'Pfam domains', 'cis-regulatory element names',
            'Protein PTMs', 'TF-TG properties', 'GWAS features', 'TWAS features',
            'cis-regulatory element families', 'Conservation features', 'SPM features', 
            'TPM features', 'Orthogroups', 'Diurnal amplitude', 'Phylostrata', 
            'Disordered domains regions', 'Transmembrane helices', 'Biochemical features',
            'Number of domains', 'PPI network features', 'Coexp network features', 
            'Regulatory network features', 'Aranet network features', 'Nucleotide Diversity']

'''
# 3 feature categories are missing
set(all_cats) - set(cat_counts)
Out[187]: {'Diurnal amplitude', 'GWAS features', 'Nucleotide Diversity'}
'''

cat_prop = cat_counts.copy()
total_value = cat_prop.sum(axis=1)
cat_prop = cat_prop.divide(total_value, axis=0)
'''
# Probably due to floating point errors, not all 1.0 values are evaluated to be
# equals to 1.0, but actually everything adds to 1
temp = cat_prop.sum(axis=1)
cat_prop.sum(axis=1) == 1.0
Out[171]: 
feat_cluster_id
1       True
2      False
3       True
4       True
5      False
 
111     True
112     True
113     True
114     True
115     True
Length: 115, dtype: bool

cat_prop.sum(axis=1)[~(cat_prop.sum(axis=1) == 1.0)]
Out[173]: 
feat_cluster_id
2     1.0
5     1.0
8     1.0
15    1.0
50    1.0
54    1.0
58    1.0
dtype: float64
'''

cat_prop.to_csv(OUTPUT, sep='\t')