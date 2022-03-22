# -*- coding: utf-8 -*-
"""
Created on 230620

@author: weixiong
Explores and prepares the list of RNA seq run IDs which I got from google docs.
"""

import pandas as pd

FILE = 'my_features_GO_prediction_edited.tsv'
OUTPUT = 'rna_seq_dl.txt'

df = pd.read_csv(FILE, sep='\t')
'''
# Annotation3 is all nan so can drop
>>> df['Annotation3'].isnull().all()
True
'''
df.drop(columns=['Annotation3'], inplace=True)
# Drop duplicate SRA IDs
dropped_df = df.drop_duplicates()
'''
# Groupby operations drop rows with nan, so need to replace it with something
# Checks that 'not_given' does not exist in my dataframe, will replace nan
# with it
>>> 'not_given'in dropped_df.values
False
'''
dropped_df =  dropped_df.fillna('not_given')
num_samples = dropped_df.groupby(['Experiment', 'Annotation1', 'Annotation2']).\
              count()
'''
# Number of rows
>>> num_samples.shape
(407, 1)
# Number of rows is unchanged, no experimental conditions has < 3 samples
>>> num_samples[num_samples['Run'] >= 3].shape
(407, 1)
# Number of unique experiment IDs
>>> len(num_samples.index.get_level_values('Experiment').unique())
112
# Number of unique run IDs
len(dropped_df['Run'].drop_duplicates())
Out[4]: 1370
'''
dropped_df.index.name = 'ID_num'
dropped_df.to_csv(OUTPUT, sep='\t')

