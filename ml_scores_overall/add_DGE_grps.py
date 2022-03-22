# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 18:51:35 2021

@author: weixiong001

Add DGE groups to DGE scores 
"""

import pandas as pd

DGE_PATH = 'D:/GoogleDrive/machine_learning/my_features/kal_sleuth_work/grouping_DGEs/DGE_category.txt'
FILE = 'dge_scores.txt'
OUTPUT = 'dge_scores_groups.txt'

df = pd.read_csv(DGE_PATH, sep='\t', index_col=0)
df2 =  pd.read_csv(FILE, sep='\t', index_col=0)

df_dge_set = set(df['Experiment'])
df2_dge_set = set(df2.index)
'''
# 12 DGEs from my orig list of DGEs are missing from the DGE features
in ml, not sure why but nvm just ignore
df_dge_set - df2_dge_set
Out[789]: 
{'dge_E-GEOD-34241_down',
 'dge_E-GEOD-34241_up',
 'dge_E-GEOD-67797_1a_down',
 'dge_E-GEOD-67797_1a_up',
 'dge_E-GEOD-67797_1b_down',
 'dge_E-GEOD-67797_1b_up',
 'dge_E-GEOD-67797_1c_down',
 'dge_E-GEOD-67797_1c_up',
 'dge_E-GEOD-69538_1a_down',
 'dge_E-GEOD-69538_1a_up',
 'dge_E-GEOD-69538_1b_down',
 'dge_E-GEOD-69538_1b_up'}

len(df_dge_set - df2_dge_set)
Out[790]: 12
df2_dge_set - df_dge_set
Out[793]: set()

# Counts of different DGE groups
combine['Category'].value_counts()
Out[885]: 
Drought stress             34
Oxidative stress           32
Seedling development       26
Development                24
Hormone response           24
Bacterial infection        20
Nutrient stress            20
DNA methylation            18
RNA metabolic process      16
Dark condition             14
DNA damage                 14
Salt stress                14
Circadian clock            14
Immune response            14
Cold stress                14
Seed development           12
Root development           10
Photorespiratory stress     8
Mitochondrial function      8
Histone methylation         8
Genetic modification        6
Flower function             6
Flower development          6
RNA processing              6
Chromatin remodeling        6
Regeneration                4
Fungal infection            4
CO2 stress                  4
Heat stress                 4
Biotic stress               4
Predation                   4
Protein methylation         4
Mechanical stimulus         4
Leaf development            4
Gene silencing              2
Meristem development        2
Shoot development           2
Light pulse                 2
Nitrosative stress          2
DNA replication             2
Shade condition             2
Chloroplast function        2
Stomatal function           2
Fungicide                   2
Salt and heat stress        2
Blue light                  2
Beneficial infection        2
Name: Category, dtype: int64
'''

mod_df = df.set_index('Experiment')
combine = pd.concat([df2, mod_df], join='inner', axis=1)

big_dict = {}
stress_stim = ['Drought stress', 'Oxidative stress', 'Nutrient stress',
               'DNA damage', 'Cold stress', 'Salt stress', 'Photorespiratory stress',
               'Heat stress', 'CO2 stress', 'Biotic stress', 'Shade condition', 
               'Mechanical stimulus', 'Light pulse', 'Nitrosative stress',
               'Salt and heat stress', 'Blue light']
gr_dev = ['Seedling development', 'Hormone response', 'Development',
          'Seed development', 'Root development', 'Flower function',
          'Flower development', 'Regeneration', 'Leaf development',
          'Meristem development', 'Shoot development']
inf_imm = ['Bacterial infection', 'Immune response', 'Fungal infection', 
           'Predation', 'Fungicide', 'Beneficial infection']
li_cica =['Dark condition', 'Circadian clock', ]
gen_mol = ['DNA methylation', 'RNA metabolic process', 'Histone methylation',
           'Mitochondrial function', 'Chromatin remodeling', 'RNA processing',
           'Genetic modification', 'Protein methylation', 'Gene silencing',
           'DNA replication', 'Chloroplast function', 'Stomatal function']
for ele in stress_stim:
    big_dict[ele] = 'stress and stimulus'
for ele in gr_dev:
    big_dict[ele] = 'growth and development'
for ele in inf_imm:
    big_dict[ele] = 'infection and immunity'
for ele in li_cica:
    big_dict[ele] = 'light and circadian'
for ele in gen_mol:
    big_dict[ele] = 'general molecular function'

combine['Big_Cat'] = combine['Category'].map(big_dict)
'''
# Ensures no nan values, means everything is replaced as expected
combine['Big_Cat'].isna().any()
Out[20]: False
'''
selected = combine.loc[:, ['Category', 'Big_Cat', 'oob_f1']]
selected.index.name = 'class label'

selected.to_csv(OUTPUT, sep='\t')




