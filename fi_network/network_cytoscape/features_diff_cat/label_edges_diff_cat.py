# -*- coding: utf-8 -*-
"""
Spyder Editor

Count number of edges per feature, and divide this number into features belonging to the same
and different category.
"""
import pandas as pd
import numpy as np

FILE = 'overall_edges.csv'
OUTPUT = 'edges_category_type.txt'

df = pd.read_csv(FILE, sep=',', index_col=0)

selected = df.loc[:, ['name']].copy()
selected['expt1_name'] = selected['name'].str.split(' \(-\) ').str[0]
selected['expt2_name'] = selected['name'].str.split(' \(-\) ').str[1]

expt1_prefix = selected['expt1_name'] .str.split('_').str[0]
expt2_prefix = selected['expt2_name'] .str.split('_').str[0]

selected['type_category'] = np.nan
selected.loc[(expt1_prefix == expt2_prefix), 'type_category'] = 'same_category'
selected.loc[~(expt1_prefix == expt2_prefix), 'type_category'] = 'diff_category'

selected.to_csv(OUTPUT, sep='\t')
