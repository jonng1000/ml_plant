# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:52:53 2020

@author: weixiong001

Based on dtypes_partial_proc.py and fully_proc.py

This script changes dtypes of df, and fills missing binary features with 0,
missing features with only three values are explained below, categorical
features are convert to dummy variables and missing ones are assigned 0
for everything, and missing numerical features are filled with median

All Int64 dtypes are binary, except for those from d2s8, which take 3 values
(0,1,2). For those, missing values filled in with 0.

Class labels are converted to nan.
"""

import numpy as np
import pandas as pd

##############################################################################
# Read file, set all binary and categorical data to categorical datatype as they
# are originally string/float/others
# PATH constant is set in case file is not found in current working directory
PATH = './'
DATA_FILE = 'test_data_nopfam.txt'

data_f = pd.read_csv(DATA_FILE, sep='\t', index_col=0)
pnas_data = ['d2s4.txt', 'd2s5.txt', 'd2s6.txt', 'd2s7.txt', 'd2s8.txt',
             'd2s9.txt', 'd2s10.txt', 'd2s11.txt', 'd2s12.txt']

def get_dtypes(temp_file, temp_path):
    '''
    From file and path names, returns a series with index as column names
    (features), and values as dtypes of features
    '''
    temp_df = pd.read_csv(temp_path + temp_file, sep='\t', index_col=0)
    dtypes = temp_df.dtypes
    return dtypes

dict_dtypes = {i:get_dtypes(i, PATH) for i in pnas_data}
# Uncomment if needed for checking
# for key in dict_dtypes:
#     print(key)
#     print(dict_dtypes[key])
#     print()

# See number of different dtypes originally, before any editing
# data_f.dtypes.astype(str).value_counts()
# Out[47]: 
# float64    96
# object     50
# dtype: int64

# This section is to break down the data types of each section of the pnas
# dataset. Note, there could be some minor differences in dtypes from looking
# at each .txt file, from the combined dataset, but its not likely to be a
# problem. No int dtypes are seen in my df, so can used this to hold binary
# values. Better not to use boolean, because even tho sklearn will convert to
# numeric, coding it as a number by myself gurantees I know exactly what is
# going on.

# data_f.dtypes[dict_dtypes['d2s4.txt'].index]
# Out[42]: 
# Expression Median (development)       float64
# Expression Max (development)          float64
# Expression Variation (development)    float64
# Expression Breadth (development)      float64
# abiotic-shoot up-regulation           float64
# abiotic-shoot down-regulation         float64
# abiotic-shoot up/down regulation      float64
# abiotic-root up-regulation            float64
# abiotic-root down-regulation          float64
# abiotic-root up/down regulation       float64
# biotic up-regulation                  float64
# biotic down-regulation                float64
# biotic up/down regulation             float64
# hormone up-regulation                 float64
# hormone down-regulation               float64
# hormone up/down regulation            float64
# dtype: object
    
#  Above is fine, d2s4.txt gene expression values

# data_f.dtypes[dict_dtypes['d2s5.txt'].index]
# Out[43]: 
#  H3K4me3               float64
# H3K9me1                float64
# H3K23ac                float64
# H3K9ac                 float64
#  H3K9me2               float64
# H3K4me1                float64
# H3K27me3               float64
# H3T3ph                 float64
# CG body methylation    float64
# dtype: object
    
data_f.rename(columns={' H3K4me3': 'H3K4me3', ' H3K9me2': 'H3K9me2'},
              inplace=True)
# Not using boolean datatype since pandas converts NaN to True for this
data_f['CG body methylation'] = data_f['CG body methylation'].astype('Int64')

# Rename and converted some of the above to the correct datatypes, the rest
# are ok. d2s5.txt epigenetic info

# data_f.dtypes.astype(str).value_counts()
# Out[49]: 
# float64    95
# object     50
# Int64       1
# dtype: int64

# data_f.dtypes[dict_dtypes['d2s6.txt'].index]
# Out[52]: 
# Co-expressed cluster at k=2000, develop    float64
# maxPCC to paralog- abiotic                 float64
# maxPCC to paralog-biotic                   float64
# maxPCC to paralog-develop                  float64
# maxPCC to paralog-hormone                  float64
# max PCC to GM-abiotic                      float64
# max PCC to SM-abiotic                      float64
# max PCC to GM-biotic                       float64
# max PCC to SM-biotic                       float64
# max PCC to GM-develop                      float64
# max PCC to SM-develop                      float64
# max PCC to GM-hormone                      float64
# max PCC to SM-hormone                      float64
# Number of domains                          float64
# Amino acid length                          float64
# Protein-protein interactions               float64
# Aranet gene-interactions                   float64
# dtype: object

#  Above is fine, d2s6.txt coexpression values, protein info,
# gene interactions

# data_f.dtypes[dict_dtypes['d2s7.txt'].index]
# Out[53]: 
# akk100_stress_fc          object
# akk200_stress_fc          object
# akk50_stress_fc           object
# c100_dev                  object
# c100_diurnal              object
# c100_stress_fc            object
# c200_dev                  object
# c200_diurnal              object
# c200_stress_fc            object
# c50_dev                   object
# c50_diurnal               object
# c50_stress_fc             object
# h100_dev_average          object
# h100_dev_complete         object
# h100_dev_ward             object
# h100_diurnal_average      object
# h100_diurnal_complete     object
# h100_diurnal_ward         object
# h100_stress_fc_average    object
# h100_stress_fc_comp       object
# h100_stress_fc_ward       object
# h200_dev_average          object
# h200_dev_complete         object
# h200_dev_ward             object
# h200_diurnal_average      object
# h200_diurnal_complete     object
# h200_diurnal_ward         object
# h200_stress_fc_average    object
# h200_stress_fc_comp       object
# h200_stress_fc_ward       object
# h50_dev_average           object
# h50_dev_complete          object
# h50_dev_ward              object
# h50_diurnal_average       object
# h50_diurnal_complete      object
# h50_diurnal_ward          object
# h50_stress_fc_average     object
# h50_stress_fc_comp        object
# h50_stress_fc_ward        object
# k100_dev                  object
# k100_diurnal              object
# k100_stress_fc            object
# k200_dev                  object
# k200_diurnal              object
# k200_stress_fc            object
# k50_dev                   object
# k50_diurnal               object
# k50_stress_fc             object
# dtype: object

coexp_clusters = dict_dtypes['d2s7.txt'].index
data_f[coexp_clusters] = data_f[coexp_clusters].astype('category')

# Converted the above to the correct datatypes, originall, they are strings.
# d2s7.txt coexp clusters info

# data_f.dtypes.astype(str).value_counts()
# Out[58]: 
# float64     95
# category    48
# object       2
# Int64        1
# dtype: int64

# data_f.dtypes[dict_dtypes['d2s8.txt'].index]
# Out[59]: 
# kmeans100_dev_sig_cluster           float64
# kmeans100_diurnal_sig_cluster       float64
# kmeans100_stress_sig_cluster        float64
# hier100-avg_dev_sig_cluster         float64
# hier100-comp_dev_sig_cluster        float64
# hier100-ward_dev_sig_cluster        float64
# hier100-avg_diurnal_sig_cluster     float64
# hier100-comp_diurnal_sig_cluster    float64
# hier100-ward_diurnal_sig_cluster    float64
# hier100-avg_stress_sig_cluster      float64
# hier100-comp_stress_sig_cluster     float64
# hier100-ward_stress_sig_cluster     float64
# c100_dev_run2_sig_cluster           float64
# c100_diurnal_run2_sig_cluster       float64
# c100_stressfc_run8_sig_cluster      float64
# akk100_stress_sig_cluster           float64
# dtype: object

m_coexp_clusters = dict_dtypes['d2s8.txt'].index
data_f[m_coexp_clusters] = data_f[m_coexp_clusters].astype('Int64')

# Check to make sure there's only 3 levels (0,1,2) for these features
# for i in m_coexp_clusters:
#     print(data_f[i].value_counts())
#     print()

# Converted the above to the correct datatypes
# d2s8.txt more coexp clusters info

# data_f.dtypes.astype(str).value_counts()
# Out[69]: 
# float64     79
# category    48
# Int64       17
# object       2
# dtype: int64

# data_f.dtypes[dict_dtypes['d2s9.txt'].index]
# Out[70]: 
# within_atha_ dNdS         float64
# alyr_ dNdS                float64
# vvin_ dNdS                float64
# ptri_ dNdS                float64
# slyc_ dNdS                float64
# osat_ dNdS                float64
# ppat_ dNdS                float64
# athal_paralog             float64
# alyrata_homolog           float64
# vvinef_homolog            float64
# ptrich_homolog            float64
# slycop_homolog            float64
# osativa_homolog           float64
# ppatens_homolog           float64
# core_eukaryotic_genome    float64
# dtype: object

to_Int64 = ['athal_paralog', 'alyrata_homolog', 'vvinef_homolog',
          'ptrich_homolog', 'slycop_homolog', 'osativa_homolog',
          'ppatens_homolog', 'core_eukaryotic_genome']

data_f[to_Int64] = data_f[to_Int64].astype('Int64')

# data_f.dtypes.astype(str).value_counts()
# Out[74]: 
# float64     71
# category    48
# Int64       25
# object       2
# dtype: int64

# Converted some of the above to the correct datatypes
# d2s9.txt evolutionary values

# data_f.dtypes[dict_dtypes['d2s10.txt'].index]
# Out[79]:
# Functional likelihood                  float64
# Gene family size                       float64
# nucleotide diversity (pi)              float64
# Max percent identity to paralogs       float64
# FayWuH                                 float64
# MK-G                                   float64
# dS to paralog                          float64
# Retention_rate                         float64
# Pseudogene                             float64
# alpha whole genome duplication         float64
# beta-gamma whole genome duplication    float64
# duplicated since A. lyrata split       float64
# Tandem duplicate                       float64
# Singleton                              float64
# dtype: object

Int64_lst = ['Pseudogene', 'alpha whole genome duplication',
           'beta-gamma whole genome duplication',
           'duplicated since A. lyrata split', 'Tandem duplicate', 'Singleton']
data_f[Int64_lst] = data_f[Int64_lst].astype('Int64')

# 'duplicated since A. lyrata split' should be binary value, not stated in supp
# data
# Converted some of the above to the correct datatypes
# d2s10.txt gene turnover values

# data_f.dtypes.astype(str).value_counts()
# Out[80]: 
# float64     65
# category    48
# Int64       31
# object       2
# dtype: int64

# data_f.dtypes[dict_dtypes['d2s11.txt'].index]
# Out[81]: 
# Duplication point    object
# dtype: object

data_f['Duplication point'] = data_f['Duplication point'].astype('category')

# Converted above to the correct datatypes
# d2s11.txt duplication pt values

# data_f.dtypes.astype(str).value_counts()
# Out[83]: 
# float64     65
# category    49
# Int64       31
# object       1
# dtype: int64

# data_f.dtypes[dict_dtypes['d2s12.txt'].index]
# Out[84]: 
# Co-localized SM gene clusters (5 genes)            float64
# Co-localized SM gene clusters (10 genes)           float64
# Co-localized PM gene clusters (5 genes)            float64
# Co-localized PM gene clusters (10 genes)           float64
# homologous_tandem_clust_100kb                      float64
# homologous_tandem_clust_same-geneclass_100kb       float64
# nonhomologous_tandem_clust_same-geneclass_100kb    float64
# nonhomologous_tandem_clust_100kb                   float64
# Metabolic tandem clusters                          float64
# dtype: object

Int64_lst2 = ['homologous_tandem_clust_100kb',
            'homologous_tandem_clust_same-geneclass_100kb',
            'nonhomologous_tandem_clust_same-geneclass_100kb',
            'nonhomologous_tandem_clust_100kb', 'Metabolic tandem clusters']
data_f[Int64_lst2] = data_f[Int64_lst2].astype('Int64')

# Converted some of the above to the correct datatypes
# d2s12.txt duplication pt values

# data_f.dtypes.astype(str).value_counts()
# Out[88]: 
# float64     60
# category    49
# Int64       36
# object       1
# dtype: int64

# Only ~16% NaNs in matrix, but they are scatterred around, as deleting
# rows/columns with NaN probably removes bulk of data 
# (refer to work on pnas done july 2019)
total_size = data_f.shape[0] * data_f.shape[1]
total_nan = data_f.isna().sum().sum()
percent_nan = total_nan / total_size * 100

##############################################################################
# Fills missing binary features with 0, and missing numerical features with
# median

# Missing binary features, and the set of features from d2s8.txt with 3 values
# (0,1,2)
# filling inplace doesnt seem to work here, get warning about setting value
# to a view
data_f.loc[:, data_f.select_dtypes(include='Int64').columns] = \
data_f.loc[:, data_f.select_dtypes(include='Int64').columns].fillna(0)

# Check if any nan remain in filled features
# data_f.select_dtypes(include='Int64').isnull().values.any()
# Out[109]: False

median = data_f.select_dtypes(include='float64').median()
float_cols = data_f.select_dtypes(include=['float64']).columns
data_f.loc[:, float_cols] = data_f.select_dtypes(include='float64').fillna(median)

# Check if any nan remain in numerical features
# dataf.select_dtypes(include='float64').isnull().values.any()
# False

# data_f.dtypes.astype(str).value_counts()
# Out[116]: 
# float64     60
# category    49
# Int64       36
# object       1
# dtype: int64

# genes x features before creating dummy features
# data_f.shape
# Out[131]: (5251, 146)

data_f['AraCyc annotation'] = np.nan

# data_f.dtypes.astype(str).value_counts()
# Out[136]: 
# float64     61
# category    49
# Int64       36
# dtype: int64

data_f = pd.get_dummies(data_f)
# After creating dummy features
# data_f.shape
# Out[141]: (5251, 4720)
# 4720-146 = 4574 additional features due to dummy features

data_f.index.name = 'Gene'
data_f.to_csv('preprocessed_data.txt', sep='\t', na_rep='NA')