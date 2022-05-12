# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:48:26 2022

@author: weixiong001

Plots heatmap showing distribution of degree across the different feature
categories
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

FILE = 'coloured_orderedl_node_topology.csv'
FIG = 'heatmap_deg.pdf'

# Calculate normalised counts per bin
def sel_bins(a_df, feat_cat):
    fc = a_df.loc[a_df['feat_category'] == feat_cat, 'Degree_log10']
    fc_bins = fc.value_counts(bins=np.linspace(0, 2.4, 11), normalize=True)
    fc_bins.name = feat_cat
    return fc_bins


# Renaming name of series with normalised proportions
def rename(series_bin, main_df):
    orig = series_bin.name
    num = '(' + str(main_df['feat_category'].value_counts()[orig]) + ')'
    temp = series_bin.name.replace('_', ' ')
    # This changes the series_bin variable in global scope
    series_bin.name = temp + ' ' + num
    return series_bin


df = pd.read_csv(FILE, sep=',', index_col=0)
df = df.reset_index()
df = df.set_index('shared name')

selected = df.loc[:, ['feat_category', 'BetweennessCentrality', 
                      'ClusteringCoefficient', 'Degree']]
selected['Degree_log10'] = np.log10(selected['Degree'])
'''
# Determing appropriate range of intervals for heatmap
max(selected['Degree_log10'])
Out[12]: 2.3654879848909
min(selected['Degree_log10'])
Out[13]: 0.0
np.linspace(0, 2.4, 11)
Out[17]: array([0.  , 0.24, 0.48, 0.72, 0.96, 1.2 , 1.44, 1.68, 1.92, 2.16, 2.4 ])
'''
'''
# Used to check sel_bin function
a_df = selected
feat_cat = 'GO_molecular_function'
'''

# Categorical features
go_bp_bins = sel_bins(selected, 'GO_biological_process')
go_mf_bins = sel_bins(selected, 'GO_molecular_function')
go_cc_bins = sel_bins(selected, 'GO_cellular_component')
pid_bins = sel_bins(selected, 'PPI clusters')
agi_bins = sel_bins(selected, 'Aranet clusters')
dge_ss_bins = sel_bins(selected, 'DGE_stress and stimulus')
dge_gd_bins = sel_bins(selected, 'DGE_growth and development')
dge_mf_bins = sel_bins(selected, 'DGE_general molecular function')
dge_ii_bins = sel_bins(selected, 'DGE_infection and immunity')
dge_lc_bins = sel_bins(selected, 'DGE_light and circadian')
cid_bins = sel_bins(selected, 'Coexp clusters')
tti_bins = sel_bins(selected, 'Regulatory clusters')
hom_bins = sel_bins(selected, 'Homolog features')
dit_bins = sel_bins(selected, 'Diurnal timepoints')
sin_bins = sel_bins(selected, 'Single copy')
tan_bins = sel_bins(selected, 'Tandemly duplicated')
gbm_bins = sel_bins(selected, 'Gene body methlyated')
# Continuous features
pfa_bins = sel_bins(selected, 'Pfam domains')
cin_bins = sel_bins(selected, 'cis-regulatory element names')
ptm_bins = sel_bins(selected, 'Protein PTMs')
ttf_bins = sel_bins(selected, 'TF-TG properties')
twa_bins = sel_bins(selected, 'TWAS features')
cif_bins = sel_bins(selected, 'cis-regulatory element families')
con_bins = sel_bins(selected, 'Conservation features')
spm_bins = sel_bins(selected, 'SPM features')
tpm_bins = sel_bins(selected, 'TPM features')
ort_bins = sel_bins(selected, 'Orthogroups')

phy_bins = sel_bins(selected, 'Phylostrata')
mob_bins = sel_bins(selected, 'Disordered domains regions')
tmh_bins = sel_bins(selected, 'Transmembrane helices')
pep_bins = sel_bins(selected, 'Biochemical features')
num_bins = sel_bins(selected, 'Number of domains')
ppi_bins = sel_bins(selected, 'PPI network features')
coe_bins = sel_bins(selected, 'Coexp network features')
ttr_bins = sel_bins(selected, 'Regulatory network features')
agn_bins = sel_bins(selected, 'Aranet network features')

# Excluded features as they are not in the network
#gwa_bins = sel_bins(selected, 'GWAS features')
#dia_bins = sel_bins(selected, 'Diurnal amplitude')
#ntd_bins = sel_bins(selected, 'Nucleotide diversity')

# Renaming names in these series
all_bins = [go_bp_bins, go_mf_bins, go_cc_bins, pid_bins, agi_bins, dge_ss_bins,
            dge_gd_bins, dge_mf_bins, dge_ii_bins, dge_lc_bins, cid_bins, 
            tti_bins, hom_bins, dit_bins, sin_bins, tan_bins, gbm_bins,
            pfa_bins, cin_bins, ptm_bins, ttf_bins,
            twa_bins, cif_bins, con_bins, spm_bins, tpm_bins, 
            ort_bins, phy_bins, mob_bins, tmh_bins, 
            pep_bins, num_bins, ppi_bins, coe_bins, ttr_bins, 
            agn_bins]

# May not need to do this, as my function changes the series name in place,
# but just do this to make my code clearer
new_bins = []
for one_bins in all_bins:
    one_bins = rename(one_bins, selected)
    new_bins.append(one_bins)

# Creating matrix for heatmap

temp = pd.concat(new_bins, axis=1)
temp = temp.transpose()

# Plotting
plt.figure(figsize=(8,18))
g = sns.heatmap(temp, cmap=sns.color_palette("rocket", 10), 
                cbar_kws={'label': 'Proportion', 
                          'ticks':[i/10 for i in range(0,11)]})
g.set(xlabel='Degree (log10)')
'''
g.get_xticks()
Out[47]: array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
'''
g.set_xticks(list(range(11)))
g.set_xticklabels(np.linspace(0, 2.4, 11))
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()