# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:29:25 2021

@author: weixiong001

Plot graphs of continuous features according to their category, names of 
specific data sets used would be the category name
"""
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'edited_contf_scores.txt'
FIG = 'spm_rsq.png'
FIG2 = 'tpm_rsq.png'
FIG3 = 'ort_rsq.png'
FIG4 = 'phy_rsq.png'
FIG5 = 'pfa_rsq.png'
FIG5A = 'pfa_rsq_v.png'
FIG6 = 'pep_rsq.png'
FIG7 = 'num_rsq.png'
FIG8 = 'ppi_rsq.png'
FIG9 = 'coe_rsq.png'
FIG10 = 'cin_rsq.png'
FIG10A = 'cin_rsq_v.png'
FIG11 = 'cif_rsq.png'
FIG12 = 'gwa_rsq.png'
FIG12A = 'gwa_rsq_v.png'
FIG13 = 'twa_rsq.png'
FIG13A = 'twa_rsq_v.png'
FIG14 = 'ttr_rsq.png'
FIG15 = 'ttf_rsq.png'
FIG15A = 'ttf_rsq_v.png'
FIG16 = 'agn_rsq.png'
FIG17 = 'con_rsq.png'
FIG17A = 'con_rsq_v.png'
FIG18 = 'ptm_rsq.png'
FIG18A = 'ptm_rsq_v.png'

data = pd.read_csv(FILE, sep='\t', index_col=0)

new_df = data

# SPM features
spm = new_df.loc[new_df.index.str.startswith('spm_'), :]
spm = spm.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plt.figure()
g = sns.barplot(data=spm, x='class_label',  y='oob_r_sq')
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()
'''
# Value that's barely below 0, isn't depicted clearly in the graph
spm
Out[98]: 
           class_label  oob_r_sq
0             spm_Stem -0.000049
1           spm_Female  0.051618
2             spm_Leaf  0.284508
3           spm_Flower  0.028109
4             spm_Male  0.607772
5            spm_Seeds  0.343751
6             spm_Root  0.297282
7  spm_Apical meristem  0.052011
8    spm_Root meristem  0.191177
'''

# TPM features
tpm = new_df.loc[new_df.index.str.startswith('tpm_'), :]
tpm = tpm.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = tpm
plt.figure()
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG2)
plt.close()

# Diurnal amplitude has only one feature, so its not plotted
dia = new_df.loc[new_df.index.str.startswith('dia_'), :]

# Orthogroups
ort = new_df.loc[new_df.index.str.startswith('ort_'), :]
ort = ort.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = ort
plt.figure()
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG3)
plt.close()
'''
# Almost perfect scores
ort
Out[128]: 
       class_label  oob_r_sq
0  ort_ath_og_size  0.981965
1  ort_all_og_size  0.984912
'''

# Phylostrata has only one feature, so its not plotted
phy = new_df.loc[new_df.index.str.startswith('phy_'), :]
'''
# Almost perfect scores
phy
Out[132]: 
       class_label  oob_r_sq
0  phy_phylostrata  0.996306
'''

# Disordered domains has only one feature, so its not plotted
mob = new_df.loc[new_df.index.str.startswith('mob_'), :]

# Pfam domains
pfa = new_df.loc[new_df.index.str.startswith('pfa_'), :]
pfa = pfa.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = pfa
g = sns.histplot(data=plot_df, bins=10, log_scale=(False, True))
g.figure.savefig(FIG5)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG5A)
plt.close()

# Transmembrane helices has only one feature, so its not plotted
tmh = new_df.loc[new_df.index.str.startswith('tmh_'), :]

# Peptide/biochemical features
pep = new_df.loc[new_df.index.str.startswith('pep_'), :]
pep = pep.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = pep
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG6)
plt.close()
'''
# Some features have almost perfect scores
pep
Out[158]: 
                model_name  oob_r_sq           time_start             time_end
class_label                                                                   
pep_aal                 rf  0.977583  30/06/2021 00:50:52  30/06/2021 00:56:06
pep_IPC_protein         rf  0.206139  30/06/2021 00:51:20  30/06/2021 00:56:48
pep_mw                  rf  0.979012  30/06/2021 00:51:14  30/06/2021 00:55:55
'''

# Number of domains
num = new_df.loc[new_df.index.str.startswith('num_'), :]
num = num.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = num
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG7)
plt.close()

# PPI network features
ppi = new_df.loc[new_df.index.str.startswith('ppi_'), :]
ppi = ppi.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = ppi
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG8)
plt.close()
'''
# 2 feature have slightly negative scores, hence its not shown on the barplot
ppi
Out[170]: 
        class_label  oob_r_sq
0  ppi_cluster_size  0.991196
1       ppi_deg_cen -0.000077
2       ppi_bet_cen -0.000068
'''

# Coexpression features
coe = new_df.loc[new_df.index.str.startswith('coe_'), :]
coe = coe.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = coe
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG9)
plt.close()
'''
# 2 feature have slightly negative scores, hence its not shown on the barplot
coe
Out[174]: 
        class_label  oob_r_sq
0       coe_deg_cen -0.000057
1       coe_bet_cen -0.000086
2  coe_cluster_size  0.951887
'''

# cis-regulatory element names 
# 82 features
# len(cin.loc[cin['oob_r_sq'] < 0, :]) -> 23 features have R sq less than 0
# but its marginally less than zero eg -0.000102, -0.000085 so histogram
# seems like it stops at 0 but in actual fact, probably slightly goes beyond 0
cin = new_df.loc[new_df.index.str.startswith('cin_'), :]
cin = cin.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = cin
g = sns.histplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG10)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG10A)
plt.close()

# cis-regulatory element families
cif = new_df.loc[new_df.index.str.startswith('cif_'), :]
cif = cif.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = cif
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG11)
plt.close()

# GWAS features
gwa = new_df.loc[new_df.index.str.startswith('gwa_'), :]
gwa = gwa.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = gwa
g = sns.histplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG12)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG12A)
plt.close()

# TWAS features
twa = new_df.loc[new_df.index.str.startswith('twa_'), :]
twa = twa.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = twa
g = sns.histplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG13)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG13A)
plt.close()

# Gene regulatory network features
# tti cluster id features have been mislabelled as ttr features
# Only have 3 ttr features
# Data used by this code has already been corrected, so code here is edited
# to reflect this
# But originally, error was discovered here, so code was written to reflect
# this
ttr = new_df.loc[new_df.index.str.startswith('ttr_'), :]
ttr = ttr.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = ttr
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG14)
plt.close()
'''
# 2 feature have slightly negative scores, hence its not shown on the barplot
ttr_true
Out[247]: 
         class_label  oob_r_sq
0   ttr_cluster_size  0.984117
18       ttr_deg_cen -0.000072
19       ttr_bet_cen -0.000074
'''

# TF-TG properties
ttf = new_df.loc[new_df.index.str.startswith('ttf_'), :]
ttf = ttf.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = ttf
g = sns.histplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG15)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG15A)
plt.close()

# Aranet gene-interactions network features
agn = new_df.loc[new_df.index.str.startswith('agn_'), :]
agn = agn.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = agn
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.savefig(FIG16)
plt.close()
'''
# 2 feature have slightly negative scores, hence its not shown on the barplot
agn
Out[257]: 
        class_label  oob_r_sq
0       agn_deg_cen -0.000064
1       agn_bet_cen -0.000059
2  agn_cluster_size  0.988868
'''

# Nucleotide Diversity has only one feature, so its not plotted
ntd = new_df.loc[new_df.index.str.startswith('ntd_'), :]

# Various conservation features 
con = new_df.loc[new_df.index.str.startswith('con_'), :]
con = con.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = con
g = sns.barplot(data=plot_df, x='class_label',  y='oob_r_sq')
g.figure.set_size_inches(7, 7)
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG17)
plt.close()
'''
# A few features have scores of near zero, hence barplot doesnt show
con
Out[318]: 
                                     class_label  oob_r_sq
0                         con_dNdS - V. vinifera -0.005051
1                           con_dNdS - A. lyrata  0.123082
2                      con_dNdS - P. trichocarpa -0.000064
3                 con_dNdS with putative paralog  0.337088
4                   con_dS with putative paralog  0.538895
5     con_Percent identity with putative paralog  0.714930
6      con_Sequence conservation in Fungi (% ID)  0.648659
7  con_Sequence conservation in Metazoans (% ID)  0.676763
8     con_Sequence conservation in plants (% ID)  0.802746
'''

# Protein PTM features
ptm = new_df.loc[new_df.index.str.startswith('ptm_'), :]
ptm = ptm.reset_index().loc[:, ['class_label', 'oob_r_sq']]
plot_df = ptm
g = sns.histplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG18)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_r_sq')
g.figure.savefig(FIG18A)
plt.close()