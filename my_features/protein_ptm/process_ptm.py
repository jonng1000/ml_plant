# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:23:06 2021

@author: weixiong001

Creates ptm feature file, main ptm file is from Plant PTM Viewer paper,
secondary ptm file is from FAT-PTM paper. Main ptm data is used as it has more
genes than the secondary ptm file

Counts ptms together with their respective amino acid residue
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


# Drop columns if only 1 gene has that feature
threshold = len(ptms) - 1
to_drop = ptms.columns[(ptms == 0).sum() == threshold]
removed = ptms.drop(columns=to_drop)

'''
removed
Out[44]: 
           ptm_ac_K  ptm_cn_C  ptm_mo_M  ...  ptm_sm_K  ptm_so_C  ptm_ub_K
locus                                    ...                              
AT1G01030         0         0         0  ...         0         0         0
AT1G01040         0         0         0  ...         0         1         0
AT1G01050         2         0         0  ...         0         1         0
AT1G01060         0         0         0  ...         0         0         0
AT1G01080         2         0         0  ...         0         0         0
            ...       ...       ...  ...       ...       ...       ...
ATMG01200         0         0         0  ...         0         0         0
ATMG01260         0         0         0  ...         0         0         0
ATMG01270         0         0         0  ...         0         1         0
ATMG01290         0         0         0  ...         0         0         0
ATMG01360         1         0         0  ...         0         0         0

[14734 rows x 58 columns]

removed.max()
Out[45]: 
ptm_ac_K     39
ptm_cn_C      3
ptm_mo_M      7
ptm_my_G      1
ptm_na_A     12
ptm_na_C      1
ptm_na_D      2
ptm_na_E      2
ptm_na_F      1
ptm_na_G      7
ptm_na_H      1
ptm_na_I      2
ptm_na_K      2
ptm_na_L      2
ptm_na_M      8
ptm_na_N      2
ptm_na_P     10
ptm_na_Q      5
ptm_na_R      4
ptm_na_S      9
ptm_na_T      4
ptm_na_V      5
ptm_na_Y      1
ptm_ng_N     16
ptm_no_C      6
ptm_nt_A     15
ptm_nt_C      5
ptm_nt_D      8
ptm_nt_E      9
ptm_nt_F      4
ptm_nt_G     35
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
##############################################################################

##############################################################################
# Secondary ptm file
# This section shows that secondary ptm file has less genes than main ptm file
# so can ignore it
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
##############################################################################

removed.to_csv(OUTPUT, sep='\t')
