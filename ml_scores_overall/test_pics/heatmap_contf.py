# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:35:55 2021

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'edited_contf_scores.txt'
FIG = 'norm_heatmap_contf.png'

def sel_bins(a_df, feat_cat):
    fc = a_df.loc[a_df.index.str.startswith(feat_cat + '_')]
    fc_bins = fc.value_counts(bins=[-0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                                    0.8, 0.9, 1], normalize=True)
    fc_bins.name = feat_cat
    return fc_bins


df = pd.read_csv(FILE, sep='\t', index_col=0)

selected = df.loc[:, 'oob_r_sq']

pfa_bins = sel_bins(selected, 'pfa')
cin_bins = sel_bins(selected, 'cin')
ptm_bins = sel_bins(selected, 'cin')
ttf_bins = sel_bins(selected, 'ttf')
gwa_bins = sel_bins(selected, 'gwa')
twa_bins = sel_bins(selected, 'gwa')
cif_bins = sel_bins(selected, 'cif')
# These feature categories have <10 features
con_bins = sel_bins(selected, 'con')
spm_bins = sel_bins(selected, 'spm')
tpm_bins = sel_bins(selected, 'tpm')
ort_bins = sel_bins(selected, 'ort')
dia_bins = sel_bins(selected, 'dia')
phy_bins = sel_bins(selected, 'phy')
mob_bins = sel_bins(selected, 'mob')
tmh_bins = sel_bins(selected, 'tmh')
pep_bins = sel_bins(selected, 'pep')
num_bins = sel_bins(selected, 'num')
ppi_bins = sel_bins(selected, 'ppi')
coe_bins = sel_bins(selected, 'coe')
ttr_bins = sel_bins(selected, 'ttr')
agn_bins = sel_bins(selected, 'agn')
ntd_bins = sel_bins(selected, 'ntd')

temp = pd.concat([pfa_bins, cin_bins, ptm_bins, ttf_bins, gwa_bins,
                  twa_bins, cif_bins, con_bins, spm_bins, tpm_bins, 
                  ort_bins, dia_bins, phy_bins, mob_bins, tmh_bins, 
                  pep_bins, num_bins, ppi_bins, coe_bins, ttr_bins, 
                  agn_bins, ntd_bins] , axis=1)
temp = temp.transpose()
plt.figure(figsize=(10,7))
g = sns.heatmap(temp, cmap='flare', cbar_kws={'label': 'Normalized'})
g.set(xlabel='oob_R_sq')
'''
# Default positions without changing xticks
g.get_xticks()
Out[322]: array([ 0.5,  1.5,  2.5,  3.5,  4.5,  5.5,  6.5,  7.5,  8.5,  9.5, 
                 10.5, 11.5])
'''
# Shift xtick positions by 0.5 to the right, add one at position 0
g.set_xticks(list(range(13)))
g.set_xticklabels([str(x/10) for x in range(-2, 11)])
g.set_yticklabels(['2761 Pfam domains','82 cis-regulatory element names',
                   '58 Protein PTMs', '76 TF-TG properties',
                   '33 GWAS features', '28 TWAS features',
                   '15 cis-regulatory element families', 
                   '9 Conservation features', '9 SPM features', 
                   '6 TPM features','2 Orthogroups', '1 Diurnal amplitude',
                   '1 Phylostrata', '1 Disordered domains regions',
                   '1 Transmembrane helices', '3 Biochemical features',
                   '2 Number of domains', '3 PPI network features',
                   '3 Coexp network features', '3 Regulatory network features',
                   '3 Aranet network features', '1 Nucleotide Diversity'])
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()
