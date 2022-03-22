# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:23:06 2021

@author: weixiong001

Creates ptm feature file, main ptm file is from Plant PTM Viewer paper,
secondary ptm file is from FAT-PTM paper. Main ptm data is used as the feature
set, and genes absent there, but in the secondary ptm file is added to this.
Ambigious ptms from secondary ptm file which cannot be mapped to ptm names in
the main ptm file are ignored.

Counts ptms together with their respective amino acid residue

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
selected['ptm_aa'] = selected[['ptm_type', 'modified_aa']].agg('_'.join, axis=1)
selected.drop(columns=['ptm_type', 'modified_aa'], inplace=True)
pri_transcript = selected.loc[df.index.str.endswith('.1'), :]
dummies = pd.get_dummies(pri_transcript, columns=['ptm_aa'],
                         prefix=['ptm'])
ptms = dummies.groupby('locus').sum()
'''
# Calculate sums for each column, to see if there's any column with only 1 count
# There is
(ptms.sum() == 1).any()
Out[79]: True
# May want to remove features if it only appears once

# 12 features w only 1 count
ptms.sum()[:31]
Out[59]: 
ptm_ac_K    7476
ptm_cn_C      82
ptm_mo_M     731
ptm_my_G      85
ptm_na_A    2310
ptm_na_C       2
ptm_na_D      37
ptm_na_E      35
ptm_na_F       3
ptm_na_G     233
ptm_na_H       4
ptm_na_I      45
ptm_na_K      25
ptm_na_L      34
ptm_na_M    1182
ptm_na_N      15
ptm_na_P      28
ptm_na_Q      21
ptm_na_R      41
ptm_na_S    1003
ptm_na_T     240
ptm_na_V     235
ptm_na_W       1
ptm_na_Y       9
ptm_ng_N    2946
ptm_no_C    1443
ptm_nt_A    2861
ptm_nt_C      46
ptm_nt_D     497
ptm_nt_E     487
ptm_nt_F     140
dtype: uint8

ptms.sum()[31:]
Out[69]: 
ptm_nt_G      935
ptm_nt_H       43
ptm_nt_I      228
ptm_nt_K      132
ptm_nt_L      282
ptm_nt_M      116
ptm_nt_N      218
ptm_nt_P      115
ptm_nt_Q      739
ptm_nt_R       64
ptm_nt_S     2376
ptm_nt_T      874
ptm_nt_V      773
ptm_nt_W       12
ptm_nt_Y      103
ptm_nu_A        6
ptm_nu_E        1
ptm_nu_M        4
ptm_nu_S        1
ptm_nu_T        2
ptm_nu_V        2
ptm_og_S      260
ptm_og_T      102
ptm_ph_S    46968
ptm_ph_T     8849
ptm_ph_Y     1051
ptm_ro_C     1976
ptm_sm_K       81
ptm_so_C     3874
ptm_ub_K     4123
dtype: int64
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
modified['ptm_aa'] = modified[['mod', 'modified_aa']].agg('_'.join, axis=1)
modified.drop(columns=['mod', 'modified_aa'], inplace=True)
# Creating counts data
dummies2 = pd.get_dummies(modified, columns=['ptm_aa'],
                          prefix=['ptm'])
ptms2 = dummies2.groupby('locus').sum()
'''
# Calculate sums for each column, to see if there's any column with only 1 count
# There is
(ptms2.sum() == 1).any()
Out[32]: True
# See features with only one count
ptms2.sum()
Out[76]: 
ptm_ac_K    385
ptm_ng_N     11
ptm_no_C     27
ptm_og_S      1
ptm_ph_S    693
ptm_ph_T    352
ptm_ph_Y    181
ptm_sm_K      1
dtype: int64
# May want to remove features if it only appears once
'''
##############################################################################

# Final processing and saving file
combined_ptm = pd.concat([ptms, ptms2])
combined_ptm.fillna(0, inplace=True)
combined = combined_ptm.astype('uint8')
'''
combined.shape
Out[31]: (15667, 61)
# Calculate sums for each column, to see if there's any column with only 1 count
# There is
(combined.sum() == 1).any()
Out[35]: True
# May want to remove features if it only appears once
# See the max values for my features
combined.sum()[:31]
Out[81]: 
ptm_ac_K    7861
ptm_cn_C      82
ptm_mo_M     731
ptm_my_G      85
ptm_na_A    2310
ptm_na_C       2
ptm_na_D      37
ptm_na_E      35
ptm_na_F       3
ptm_na_G     233
ptm_na_H       4
ptm_na_I      45
ptm_na_K      25
ptm_na_L      34
ptm_na_M    1182
ptm_na_N      15
ptm_na_P      28
ptm_na_Q      21
ptm_na_R      41
ptm_na_S    1003
ptm_na_T     240
ptm_na_V     235
ptm_na_W       1
ptm_na_Y       9
ptm_ng_N    2957
ptm_no_C    1470
ptm_nt_A    2861
ptm_nt_C      46
ptm_nt_D     497
ptm_nt_E     487
ptm_nt_F     140
dtype: int64

combined.sum()[31:]
Out[82]: 
ptm_nt_G      935
ptm_nt_H       43
ptm_nt_I      228
ptm_nt_K      132
ptm_nt_L      282
ptm_nt_M      116
ptm_nt_N      218
ptm_nt_P      115
ptm_nt_Q      739
ptm_nt_R       64
ptm_nt_S     2376
ptm_nt_T      874
ptm_nt_V      773
ptm_nt_W       12
ptm_nt_Y      103
ptm_nu_A        6
ptm_nu_E        1
ptm_nu_M        4
ptm_nu_S        1
ptm_nu_T        2
ptm_nu_V        2
ptm_og_S      261
ptm_og_T      102
ptm_ph_S    47661
ptm_ph_T     9201
ptm_ph_Y     1232
ptm_ro_C     1976
ptm_sm_K       82
ptm_so_C     3874
ptm_ub_K     4123
dtype: int64
'''

'''
# See which features only have 1 count, also checks to see if there's any 0,
# shouldn't have
combined.columns[combined.sum() <= 1]
Out[84]: Index(['ptm_na_W', 'ptm_nu_E', 'ptm_nu_S'], dtype='object')
'''

new_comb = combined.drop(columns=['ptm_na_W', 'ptm_nu_E', 'ptm_nu_S'])
'''
# Check to see if any genes doesn't have any values, if so, genes need to be
# dropped
# This is not the case
(new_comb.sum(axis=1) == 0).any()
Out[91]: False

new_comb.shape
Out[92]: (15667, 58)
'''

'''
# Just exploring the max values
new_comb.max()[:31]
Out[107]: 
ptm_ac_K    39
ptm_cn_C     3
ptm_mo_M     7
ptm_my_G     1
ptm_na_A    12
ptm_na_C     1
ptm_na_D     2
ptm_na_E     2
ptm_na_F     1
ptm_na_G     7
ptm_na_H     1
ptm_na_I     2
ptm_na_K     2
ptm_na_L     2
ptm_na_M     8
ptm_na_N     2
ptm_na_P    10
ptm_na_Q     5
ptm_na_R     4
ptm_na_S     9
ptm_na_T     4
ptm_na_V     5
ptm_na_Y     1
ptm_ng_N    16
ptm_no_C     6
ptm_nt_A    15
ptm_nt_C     5
ptm_nt_D     8
ptm_nt_E     9
ptm_nt_F     4
ptm_nt_G    35
dtype: uint8

new_comb.max()[31:]
Out[108]: 
ptm_nt_H      4
ptm_nt_I      4
ptm_nt_K      4
ptm_nt_L      7
ptm_nt_M      4
ptm_nt_N      5
ptm_nt_P      8
ptm_nt_Q      7
ptm_nt_R      3
ptm_nt_S     25
ptm_nt_T     39
ptm_nt_V      8
ptm_nt_W      3
ptm_nt_Y     13
ptm_nu_A      1
ptm_nu_M      1
ptm_nu_T      1
ptm_nu_V      1
ptm_og_S     11
ptm_og_T      5
ptm_ph_S    150
ptm_ph_T     43
ptm_ph_Y     17
ptm_ro_C     15
ptm_sm_K      3
ptm_so_C     16
ptm_ub_K     40
dtype: uint8
'''

new_comb.to_csv(OUTPUT, sep='\t')
