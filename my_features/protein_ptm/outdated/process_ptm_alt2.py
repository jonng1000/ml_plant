# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:23:06 2021

@author: weixiong001

Creates ptm feature file, main ptm file is from Plant PTM Viewer paper,
secondary ptm file is from FAT-PTM paper. Main ptm data is used as the feature
set, and genes absent there, but in the secondary ptm file is added to this.
Ambigious ptms from secondary ptm file which cannot be mapped to ptm names in
the main ptm file are ignored.

Counts ptms and modified amino acid names

Alt way of producing ptm features, but this method is not used so ignore
"""

import pandas as pd

FILE = 'all_PTMs_ath.tab'
FILE2 = 'ptms.tsv'
OUTPUT = 'ptm_features.txt'

##############################################################################
# Main ptm file
df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# Total number of unique gene ids, including isoforms
len(set(df['locus']))
Out[43]: 14820
# Total number of primary transcripts, denoted by .1
len(set(df.index[df.index.str.endswith('.1')]))
Out[48]: 14734
all_trans = set(df['locus'])
pri_trans = set(df.index[df.index.str.endswith('.1')])
mod_pri = {x.split('.')[0] for x in pri_trans}
wo_pri = all_trans - mod_pri
# Only 86 genes don't have primary transcripts, so can ignore them
'''
# Creating counts info
selected = df.loc[:, ['ptm_type', 'modified_aa', 'locus']]
pri_transcript = selected.loc[df.index.str.endswith('.1'), :]
dummies = pd.get_dummies(pri_transcript, columns=['ptm_type', 'modified_aa'],
                         prefix=['ptm', 'ptm'])
ptms = dummies.groupby('locus').sum()
'''
# Calculate sums for each column, to see if there's any column with only 1 count
# There isnt
(ptms.sum() == 1).any()
Out[79]: False
# May want to remove features if it only appears once
'''
##############################################################################

##############################################################################
# Secondary ptm file
df2 = pd.read_csv(FILE2, sep='\t', index_col=0)
'''
# Total number of unique gene ids, including isoforms
temp = [x[0] for x in df2.index.str.split('.')]
len(set(temp))
Out[95]: 10850
# Total number of primary transcripts, denoted by .1
len(set(df2.index[df2.index.str.endswith('.1')]))
10596
len(set(temp)) - len(set(df2.index[df2.index.str.endswith('.1')]))
Out[96]: 254
# Abour 250+ genes do not have primary transcripts
'''
# Finding the set of genes which are missing from main ptm file
df2_genes = df2.index.str.split('.').str[0]
missing = set(df2_genes) - set(ptms.index)
df2['locus'] = df2_genes
missing_df2 = df2.loc[df2['locus'].isin(missing), :]
'''
len(set(missing_df2['locus']))
Out[127]: 1002
len(set(missing_df2.index[missing_df2.index.str.endswith('.1')]))
Out[129]: 951
# Only 51 missing genes do not have primary transcripts, so can ignore them
'''
# Missig genes
missing_pri = missing_df2.loc[missing_df2.index.str.endswith('.1'), :]
'''
len(set(missing_pri.index))
Out[140]: 951
'''

# Mapping ptm names from secondary ptm file to main file, ignore those which
# are ambigious and cannot be mapped
# acylation can be myristoylation or palmitoylation, ambigious
# ubiquitinylation can be wrt to lysine or n-term one, ambigious
map_dict = {'ACETYLATION': 'ac', 'N-GLYCOSYLATION': 'ng', 'O-GLCNAC': 'og',
            'PHOSPHORYLATION': 'ph', 'S-NITROSYLATION': 'no',
            'SUMOYLATION': 'sm'}

'''
# Exploring data
missing_pri['mod'].value_counts()
Out[136]: 
PHOSPHORYLATION    1226
ACETYLATION         385
S-NITROSYLATION      27
UBIQUITINATION       24
N-GLYCOSYLATION      11
O-GLCNAC              1
SUMOYLATION           1
Name: mod, dtype: int64
# Seeing how much data i miss if I drop this
len(set(missing_pri.loc[missing_pri['mod'] == 'UBIQUITINATION', :].index))
Out[139]: 21
'''
# Remove ambigious ptms
rem_ubi = missing_pri.loc[missing_pri['mod'] != 'UBIQUITINATION', :]
'''
len(set(rem_ubi.index))
Out[143]: 933
'''
# Renaming ptms to make it the same as in the main ptm file
replace_ptm = rem_ubi.replace({'mod': map_dict})
modified = replace_ptm.set_index('locus').drop(columns=['count'])
modified['modified_aa'] = modified['site'].str[0]
modified.drop(columns=['site'], inplace=True)
# Creating counts data
dummies2 = pd.get_dummies(modified, columns=['mod', 'modified_aa'],
                          prefix=['ptm', 'ptm'])
ptms2 = dummies2.groupby('locus').sum()
'''
# Calculate sums for each column, to see if there's any column with only 1 count
# There is
(ptms2.sum() == 1).any()
Out[32]: True
# May want to remove features if it only appears once
'''
##############################################################################

# Final processing and saving file
combined_ptm = pd.concat([ptms, ptms2])
combined_ptm.fillna(0, inplace=True)
combined = combined_ptm.astype('uint8')
'''
combined.shape
Out[31]: (15667, 35)
# Calculate sums for each column, to see if there's any column with only 1 count
# There isnt
(combined.sum() == 1).any()
Out[35]: False
# May want to remove features if it only appears once
# See the max values for my features
combined.max()
Out[38]: 
ptm_ac     39
ptm_cn      3
ptm_mo      7
ptm_my      1
ptm_na     17
ptm_ng     16
ptm_no      6
ptm_nt    148
ptm_nu      1
ptm_og     14
ptm_ph    164
ptm_ro     15
ptm_sm      3
ptm_so     16
ptm_ub     40
ptm_A      22
ptm_C      22
ptm_D       9
ptm_E       9
ptm_F       4
ptm_G      35
ptm_H       4
ptm_I       6
ptm_K      55
ptm_L       8
ptm_M      11
ptm_N      16
ptm_P      18
ptm_Q      11
ptm_R       7
ptm_S     153
ptm_T      54
ptm_V      11
ptm_W       3
ptm_Y      17
dtype: uint8
'''

combined.to_csv(OUTPUT, sep='\t')
