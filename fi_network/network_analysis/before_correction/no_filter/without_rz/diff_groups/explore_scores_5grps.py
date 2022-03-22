# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 12:20:39 2021

@author: weixiong001

Plots score distribution of 5 feature categories
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'big_scores.txt'
FIG = 'grps5_hist_step.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)

selected = df.loc[:, ['oob_f1', 'oob_r_sq']].copy()
selected.insert(0, 'category', np.nan)

selected.loc[selected.index.str.startswith('go_'), 'category'] = 'GO'
selected.loc[selected.index.str.startswith(('spm_', 'tpm_', 'dge_', 'dia_',
                                            'dit_')), 
             'category'] = 'Expression'
selected.loc[selected.index.str.startswith(('mob_', 'pfa_', 'tmh_', 'num_')), 
             'category'] = 'Protein Domain'

networks = ('ppi_', 'pid_', 'coe_', 'cid_', 'ttr_', 'tti_', 'ttf_', 'agn_', 'agi_')
selected.loc[selected.index.str.startswith(networks), 'category'] = 'Networks'

others = ('ort_', 'phy_', 'sin_', 'tan_', 'pep_', 'cin_', 'cif_', 'gwa_', 
          'twa_', 'hom_', 'ntd_', 'gbm_', 'con_', 'ptm_')
selected.loc[selected.index.str.startswith(others), 'category'] = 'Others'

selected['scores'] = selected['oob_f1'].copy()
selected['scores'] = selected['scores'].fillna(selected['oob_r_sq'])

plt.figure(figsize=(15,7))
g = sns.histplot(data=selected, x='scores', hue='category', element='step', 
                 bins=15, log_scale=(False, True))
g.figure.savefig(FIG)
plt.close()
