# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:29:25 2021

@author: weixiong001

Plot graphs of categorical features according to their category, names of 
specific data sets used would be the category name
"""
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'edited_catf_scores.txt'
FIG = 'dit_f1.png'
FIG2 = 'pid_f1.png'
FIG2A = 'pid_f1_v.png'
FIG3 = 'cid_f1.png'
FIG3A = 'cid_f1_v.png'
FIG4 = 'tti_f1.png'
FIG4A = 'tti_f1_v.png'
FIG5 = 'agi_f1.png'
FIG5A = 'agi_f1_v.png'
FIG6 = 'hom_f1.png'
FIG6A = 'hom_f1_v.png'

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

dit = new_df.loc[new_df.index.str.startswith('dit_'), :]
dit = dit.reset_index().loc[:, ['class_label', 'oob_f1']]
plt.figure()
g = sns.barplot(data=dit, x='class_label',  y='oob_f1')
g.xaxis.set_tick_params(rotation=90)
plt.tight_layout()
g.figure.savefig(FIG)
plt.close()

# Single copy genes has only one feature, so its not plotted
sin = new_df.loc[new_df.index.str.startswith('sin_'), :]

# Tandemly duplicated genes has only one feature, so its not plotted
tan = new_df.loc[new_df.index.str.startswith('tan_'), :]

pid = new_df.loc[new_df.index.str.startswith('pid_'), :]
pid = pid.reset_index().loc[:, ['class_label', 'oob_f1']]
plot_df = pid
plt.figure()
g = sns.histplot(data=plot_df, log_scale=(False, True))
g.figure.savefig(FIG2)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_f1')
g.figure.savefig(FIG2A)
plt.close()

cid = new_df.loc[new_df.index.str.startswith('cid_'), :]
cid = cid.reset_index().loc[:, ['class_label', 'oob_f1']]
plot_df = cid
g = sns.histplot(data=plot_df)
g.figure.savefig(FIG3)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_f1')
g.figure.savefig(FIG3A)
plt.close()

tti = new_df.loc[new_df.index.str.startswith('tti_'), :]
tti = tti.reset_index().loc[:, ['class_label', 'oob_f1']]
plot_df = tti
g = sns.histplot(data=plot_df)
g.figure.savefig(FIG4)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_f1')
g.figure.savefig(FIG4A)
plt.close()

agi = new_df.loc[new_df.index.str.startswith('agi_'), :]
agi = agi.reset_index().loc[:, ['class_label', 'oob_f1']]
plot_df = agi
g = sns.histplot(data=plot_df, log_scale=(False, True))
g.figure.savefig(FIG5)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_f1')
g.figure.savefig(FIG5A)
plt.close()

hom = new_df.loc[new_df.index.str.startswith('hom_'), :]
hom = hom.reset_index().loc[:, ['class_label', 'oob_f1']]
plot_df = hom
g = sns.histplot(data=plot_df)
g.figure.savefig(FIG6)
plt.close()
g = sns.violinplot(data=plot_df, x='oob_f1')
g.figure.savefig(FIG6A)
plt.close()

# Gene body methlyated has only one feature, so its not plotted
gbm = new_df.loc[new_df.index.str.startswith('gbm_'), :]