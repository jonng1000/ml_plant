# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:31:44 2020

@author: weixiong001

Labels my ml dataset with class labels, based on label_ml_data.py, but does
it for all 16 GO classes selected by Marek, hence it has a new name.
All labels will have values of either 0 or 1, depending if the gene
has that label or not

Takes ~5 min to run
"""
import pandas as pd
import numpy as np

GO_SELECT = 'D:/GoogleDrive/machine_learning/GO_labels/marek_selections.txt'
ML_DATA = 'ml_dataset.txt'
ML_DATA_LABEL = 'ml_16_labels.txt'

# Marek selections file
colnames=['GO class', 'number', 'GO cat', 'GO name', 'genes'] 
selection = pd.read_csv(GO_SELECT, sep="\t", names=colnames, header=None)
# My ml data file
data = pd.read_csv(ML_DATA, sep='\t', index_col=0)

# Get all 16 class labels and convert them into binary values, to indicate
# if the gene has that label or not
selection.loc[:, ['genes']] = selection['genes'].str.split(' ')
one_gene_cp = selection.explode('genes').loc[:, ['GO name', 'genes']]
one_gene_cp = one_gene_cp.set_index('genes')
binary_labels = pd.get_dummies(one_gene_cp, prefix='class_label')
# These combine duplicated genes into the same row, as the same
# gene occuplies multiple rows if it has >1 cell part label
# After combining duplicates, each row has one gene, with all its
# labels
# Multiple identical indexes throws an error when pd.concat is used
combined_rows = binary_labels.groupby(binary_labels.index).sum()
'''
# Check to make sure entire df has only 0 and 1 values after combing
np.unique(combined_rows.values)
Out[122]: array([0, 1], dtype=uint8)
# Has non AT- labelled genes, but nvm, just ignore
combined_rows.index[~combined_rows.index.str.startswith('AT')]
Out[130]: Index(['KOD', 'RPW8.2'], dtype='object', name='genes')
'''

bl_col_names = combined_rows.columns
# Combines cell parts labels with feature data, and fills nans in labels
# with 0s
all_labels = pd.concat([data, combined_rows], axis=1)
zero_map = {name:0 for name in bl_col_names}
all_labels.fillna(zero_map, inplace=True)
'''
# Check to ensure that only the cell parts class labels have nan
# filled as 0s, and other columns do not have thid
all_labels.loc[:, bl_col_names].isna().any().any()
Out[62]: False
all_labels.isna().any().any()
Out[63]: True
'''
'''
all_labels.index[all_labels.index.str.startswith('AT')]
Out[150]: 
Index(['ATCG00500', 'ATCG00510', 'ATCG00280', 'ATCG00890', 'ATCG01250',
       'ATCG00180', 'ATCG00340', 'ATCG00420', 'ATCG00600', 'ATCG00210',
       ...
       'AT5G65533', 'AT5G66211', 'AT1G64633', 'AT1G13840', 'AT1G21529',
       'AT4G03060-CVI', 'AT4G16355', 'AT4G16730-WS', 'ATBP2', 'ATMG00930'],
      dtype='object', name='Gene', length=29676)

all_labels[all_labels.index.str.startswith('AT')]
Out[151]: 
               pep_aal  ...  class_label_vacuole
Gene                    ...                     
ATCG00500        488.0  ...                  0.0
ATCG00510         37.0  ...                  0.0
ATCG00280        473.0  ...                  0.0
ATCG00890        389.0  ...                  0.0
ATCG01250        389.0  ...                  0.0
               ...  ...                  ...
AT4G03060-CVI      NaN  ...                  0.0
AT4G16355          NaN  ...                  0.0
AT4G16730-WS       NaN  ...                  0.0
ATBP2              NaN  ...                  0.0
ATMG00930          NaN  ...                  0.0

[29676 rows x 6449 columns]
'''
all_labels.index.name = 'Gene'

all_labels.to_csv(ML_DATA_LABEL, na_rep='NA', sep='\t')


