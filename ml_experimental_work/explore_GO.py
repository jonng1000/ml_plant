# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:39:48 2022

@author: weixiong001

For getting all GO terms from GO database, explore and clean data, and get
GO features for ml
"""

import pandas as pd

FILE = './tair_gaf/tair.gaf'
OUTPUT = 'atg_GO_features.txt'
OUTPUT2 = 'AT1G04250_GO_features.txt'
OUTPUT3 = 'atg_GO_features_corrected.txt'

names_l = [i for i in range(17)]
df = pd.read_csv(FILE, sep='\t', comment='!', names=names_l,
                 header=None)
df.rename(columns={0:'DB', 1: 'DB Object ID', 2:'DB Object Symbol', 
                   3:'Qualifier', 4:'GO ID', 6:'Evidence Code', 
                   8: 'Aspect'},
          inplace=True)

atg_names = df.loc[df['DB Object ID'].str.contains('^AT[1-5|M|C]G[0-9]{4}[0-9]$', regex=True), :]

##############################################################################
# Exploratory work, realised there multiple duplicate GO terms are assigned
# to each gene, so need to remove duplicates
'''
# Number of genes, repeated
atg_names.shape
Out[10]: (211187, 17)

# Number of unique genes
atg_names['DB Object ID'].unique()
Out[7]: 
array(['AT1G11880', 'AT1G80420', 'AT2G36530', ..., 'AT3G05890',
       'AT1G62900', 'AT1G68370'], dtype=object)

len(atg_names['DB Object ID'].unique())
Out[8]: 28872
'''
'''
temp = df.loc[~df['DB Object ID'].str.contains('^AT[1-5|M|C]G[0-9]{4}[0-9]$', regex=True), :]
temp = temp.copy()
temp['DB Object Symbol'] = temp['DB Object Symbol'].str.upper()
temp_restrict = temp.loc[temp['DB Object Symbol'].str.contains('^AT[1-5|M|C]G[0-9]{4}[0-9]$', regex=True), :]

temp_restrict.shape
Out[31]: (8766, 17)

# Only about 4% new features here then compared to the original feature set
# above, so can ignore these
8766/211187*100
Out[27]: 4.150823677593792
'''

atg_GO = atg_names.loc[:, ['DB Object ID', 'GO ID', 'Evidence Code']]
atg_dummies = pd.get_dummies(atg_GO, columns=['GO ID'], prefix=['go'])
"""
# Commented out this chunk to save time, just for checking
atg_GO_counts = atg_dummies.groupby('DB Object ID').sum()
'''
# Check to ensure there's only 0 or 1 values, but this is not true due to
# duplicate values
test = atg_GO_counts.values.reshape(-1)
test.sort()

test
Out[48]: array([  0,   0,   0, ..., 108, 109, 118], dtype=uint8)
'''
atg_GO_counts.index.name = 'Gene'
atg_GO_counts.to_csv(OUTPUT, sep='\t')
'''
go_GO:0005515 -> from excel sheet, this GO term has 108 counts
'''
AT1G04250 = df.loc[df['DB Object ID'] == 'AT1G04250', :]
AT1G04250.index.name = 'id'
AT1G04250.to_csv(OUTPUT2, sep='\t')
"""
##############################################################################

atg_dummies_drop = atg_dummies.drop(columns=['Evidence Code'])
atg_dummies_nodup = atg_dummies_drop.drop_duplicates()
atg_GO_freq = atg_dummies_nodup.groupby('DB Object ID').sum()
'''
#  Check to ensure only 0 and 1 values, which is true
test = atg_GO_freq.values.reshape(-1)
test.sort()

test
Out[9]: array([0, 0, 0, ..., 1, 1, 1], dtype=uint8)
'''
atg_GO_freq.index.name = 'Gene'
atg_GO_freq.to_csv(OUTPUT3, sep='\t')
