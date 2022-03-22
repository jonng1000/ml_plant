# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:31:41 2021

@author: weixiong001

OHE features from tran-eQTL from AtMAD. These are SNPs far genes,
which are correlated with their expression levels.
"""
import pandas as pd

FILE = 'transeqtl.txt'
OUTPUT = 'processed_trans_qtl.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# Check that all data points here are statistically significant
significance = df['FDR'] < 0.05
significance.all()
Out[10]: True
'''
reset = df.reset_index()
gene_index = reset.set_index('Gene')
features = gene_index.loc[:, ['SNP', 'Alleles']].agg('_'.join, axis=1)
ohe_features = pd.get_dummies(features, prefix='tsn')
'''
ohe_features.shape
Out[34]: (10118, 6776)
'''
ohe_features.to_csv(OUTPUT, sep='\t')