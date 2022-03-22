# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:52:53 2020

@author: weixiong001

This script changes dtypes of df, and fills missing binary features with 0,
and missing numerical features with median. Leaves missing categorical
features and class labels alone.
"""

import numpy as np
import pandas as pd

##############################################################################
# Read file, set all binary and categorical data to categorical datatype as they
# are originally string/float/others

path = 'D:/GoogleDrive/machine learning/GMSM ML/building_pnas_dataset_JN/'
file = 'combined_data_II.txt'
df = pd.read_csv(path + file, sep='\t', index_col=0)

pnas_data = ['d2s4.txt', 'd2s5.txt', 'd2s6.txt', 'd2s7.txt', 'd2s8.txt',
             'd2s9.txt', 'd2s10.txt', 'd2s11.txt', 'd2s12.txt', 'd2s13.txt']

def get_dtypes(temp_file, temp_path):
    '''
    
    Parameters
    ----------
    temp_file : string
        file name
    path : string
        file path

    Returns
    -------
    dtypes : pandas series
        Series with index as column nanes, and values as dtypes

    '''
    temp_df = pd.read_csv(temp_path + temp_file, sep='\t', index_col=0)
    dtypes = temp_df.dtypes
    return dtypes

dict_dtypes = {i:get_dtypes(i, path) for i in pnas_data}
# Comment out these lines because I only need to run once
# for key in dict_dtypes:
#     print(key)
#     print(dict_dtypes[key])
#     print()

# This section is to break down the data types of each section of the pnas
# dataset. Note, there could be some minor differences in dtypes from looking
# at each .txt file, from the combined dataset, but its not likely to be a
# problem. No int dtypes are seen in my df, so can used this to hold binary
# values. Better not to use boolean, because even tho sklearn will convert to
# numeric, coding it as a number by myself gurantees I know exactly what is
# going on.

# d2s4.txt
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

# d2s5.txt
#   H3K4me3               float64
# H3K9me1                float64
# H3K23ac                float64
# H3K9ac                 float64
#   H3K9me2               float64
# H3K4me1                float64
# H3K27me3               float64
# H3T3ph                 float64
# CG body methylation    float64
# dtype: object
    
df.rename(columns={' H3K4me3': 'H3K4me3', ' H3K9me2': ' H3K9me2'},
          inplace=True)
# Not using boolean datatype since pandas converts NaN to True for this
df['CG body methylation'] = df['CG body methylation'].astype('category')

# Rename and converted some of the above to the correct datatypes, the rest
# are ok
# d2s5.txt epigenetic info

# d2s6.txt
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

# d2s7.txt
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
df[coexp_clusters] = df[coexp_clusters].astype('category')

# Converted the above to the correct datatypes
# d2s7.txt coexp clusters info

# d2s8.txt
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
# akk100_stress_sig_cluster             int64
# dtype: object

m_coexp_clusters = dict_dtypes['d2s8.txt'].index
df[m_coexp_clusters] = df[m_coexp_clusters].astype('category')

# Converted the above to the correct datatypes
# d2s8.txt more coexp clusters info

# d2s9.txt
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

to_cat = ['athal_paralog', 'alyrata_homolog', 'vvinef_homolog',
          'ptrich_homolog', 'slycop_homolog', 'osativa_homolog',
          'ppatens_homolog', 'core_eukaryotic_genome']

df[to_cat] = df[to_cat].astype('category')

# Converted some of the above to the correct datatypes
# d2s9.txt evolutionary values

# d2s10.txt
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

cat_lst = ['Pseudogene', 'alpha whole genome duplication',
           'beta-gamma whole genome duplication',
           'duplicated since A. lyrata split', 'Tandem duplicate', 'Singleton']
df[cat_lst] = df[cat_lst].astype('category')

# 'duplicated since A. lyrata split' should be binary value, not stated in supp
# data
# Converted some of the above to the correct datatypes
# d2s10.txt gene turnover values

# d2s11.txt
# Duplication point    object
# dtype: object

df['Duplication point'] = df['Duplication point'].astype('category')

# Converted above to the correct datatypes
# d2s11.txt duplication pt values

# d2s12.txt
# df              int64
# Co-localized SM gene clusters (10 genes)             int64
# Co-localized PM gene clusters (5 genes)              int64
# Co-localized PM gene clusters (10 genes)             int64
# homologous_tandem_clust_100kb                        int64
# homologous_tandem_clust_same-geneclass_100kb         int64
# nonhomologous_tandem_clust_same-geneclass_100kb      int64
# nonhomologous_tandem_clust_100kb                     int64
# Metabolic tandem clusters                          float64
# dtype: object

cat_lst2 = ['homologous_tandem_clust_100kb',
            'homologous_tandem_clust_same-geneclass_100kb',
            'nonhomologous_tandem_clust_same-geneclass_100kb',
            'nonhomologous_tandem_clust_100kb', 'Metabolic tandem clusters']
df[cat_lst2] = df[cat_lst2].astype('category')

# Converted some of the above to the correct datatypes
# d2s12.txt duplication pt values

# d2s13.txt
# NOGCT              float64
# NOG1               float64
# MMR_HSR1           float64
# FeoB_N             float64
# DUF4283            float64
  
# COX2               float64
# COX1               float64
# CcmF_C             float64
# Mt_ATP-synt_B      float64
# gag_pre-integrs    float64
# Length: 4217, dtype: object

domains = dict_dtypes['d2s13.txt'].index
# This step takes very long, 5min
df.loc[:, domains] = df.loc[:, domains].astype('category')
#df[domains] = df[domains].astype('category')

# Only ~15% NaNs in matrix, but they are scatterred around, as deleting
# rows/columns with NaN removes bulk of data (refer to work on pnas done
# july 2019)
total_size = df.shape[0]*df.shape[1]
total_nan = df.isna().sum().sum()
percent_nan = df.isna().sum().sum() / (df.shape[0]*df.shape[1]) * 100

# df.dtypes.astype(str).value_counts()
# Out[140]: 
# category    4302
# float64      629
# object         1
# dtype: int64

##############################################################################
# Fills missing binary features with 0, and missing numerical features with
# median

bin_features = ['CG body methylation'] + to_cat + cat_lst + cat_lst2 + \
    list(domains)
# inplace doesnt seem to work heere
df.loc[:, bin_features] = df.loc[:, bin_features].fillna(0)
df.loc[:, bin_features] = df.loc[:, bin_features].astype('int64')

# df.dtypes.astype(str).value_counts()
# int64       4237
# float64      629
# category      65
# object         1
# dtype: int64

# Check if any nan remain in binary features
# df.select_dtypes(include='int64').isnull().values.any()
# False

# Metabolic pathway features, also binary in nature, so need to do the same
# as above
pathway_features = df.filter(like='|').columns
df.loc[:, pathway_features] = df.loc[:, pathway_features].fillna(0)
df.loc[:, pathway_features] = df.loc[:, pathway_features].astype('int64')

median = df.select_dtypes(include='float64').median()
float_cols = df.select_dtypes(include=['float64']).columns
df.loc[:, float_cols] = df.select_dtypes(include='float64').fillna(median)

# Check if any nan remain in numerical features
# df.select_dtypes(include='float64').isnull().values.any()
# 

# df.dtypes.astype(str).value_counts()
# int64       4806
# category      65
# float64       60
# object         1
# dtype: int64

cat_features = df.select_dtypes(include='category').columns
cat_features.to_series(index=range(0,len(cat_features))) \
    .to_csv('cat_features.txt', sep='\t')
# This step takes very long, 5min
df.to_csv('partial_processed.txt', sep='\t')
