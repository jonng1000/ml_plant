# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:20:16 2019

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

labels_df = pd.read_csv("PNAS_labels.txt", sep="\t", index_col=0)
#labels_df["GO_annotation"].value_counts()
#Out[25]: 
#none                                                     2697
#Primary metabolic process                                1848
#Secondary metabolic process                               233
#Primary metabolic process-Secondary metabolic process     155
#Name: GO_annotation, dtype: int64
#
#labels_df["AraCyc_annotation"].value_counts()
#Out[26]: 
#none                                             2933
#Non-secondary metabolism pathway                 1306
#Secondary metabolism pathway                      423
#Seconday and Non-secondary metabolism pathway     264
#Name: AraCyc_annotation, dtype: int64
labels_df["GO_annotation"] = labels_df["GO_annotation"].str.replace(
        'Primary metabolic process', 'GM', regex=False)
labels_df["GO_annotation"] = labels_df["GO_annotation"].str.replace(
        'Secondary metabolic process', 'SM', regex=False)
labels_df["AraCyc_annotation"] = labels_df["AraCyc_annotation"].str.replace(
        'Non-secondary metabolism pathway', 'GM', regex=False)
labels_df["AraCyc_annotation"] = labels_df["AraCyc_annotation"].str.replace(
        'Secondary metabolism pathway', 'SM', regex=False)
labels_df["AraCyc_annotation"] = labels_df["AraCyc_annotation"].str.replace(
        'Seconday and GM', 'GM-SM', regex=False)

df = pd.read_csv("combined_data_ML.csv", sep="\t", index_col=0)
pnas_df = pd.concat([df, labels_df["AraCyc_annotation"]], axis=1, sort=False)

pndf_GMSM = pnas_df.loc[(pnas_df['AraCyc_annotation'] == 'GM') |
        (pnas_df['AraCyc_annotation'] == 'SM')]

# Most nan values are in var_median, so can drop rows with nan in categorical
# values.
#pndf_GMSM.isna().sum()
#Out[65]: 
#mean_exp               2
#median_exp             2
#max_exp                2
#min_exp                2
#var_exp                2
#var_median           224
#OG_size               16
#taxon                 16
#single_copy           16
#tandem_dup             1
#Category               1
#AraCyc_annotation      0
#dtype: int64

drop_cat = pndf_GMSM.dropna(subset=['taxon', 'single_copy', 'tandem_dup'])
drop_cat = drop_cat.drop(columns=['Category'])
#drop_cat.isna().sum()
#Out[70]: 
#mean_exp               1
#median_exp             1
#max_exp                1
#min_exp                1
#var_exp                1
#var_median           214
#OG_size                0
#taxon                  0
#single_copy            0
#tandem_dup             0
#AraCyc_annotation      0
#dtype: int64
filled_nan = drop_cat.fillna(drop_cat.median())
filled_nan.isna().sum()
#Out[73]: 
#mean_exp             0
#median_exp           0
#max_exp              0
#min_exp              0
#var_exp              0
#var_median           0
#OG_size              0
#taxon                0
#single_copy          0
#tandem_dup           0
#AraCyc_annotation    0
#dtype: int64

fig, ax = plt.subplots(figsize=(12,12))
sns.heatmap(filled_nan.corr(method='pearson'), ax=ax)
plt.savefig("heatmap_corr_pnas.png")

filled_nan.rename(columns={"AraCyc_annotation": "Category"}, inplace=True)
#filled_nan['Category'].value_counts()
#Out[102]: 
#GM    1295
#SM     418
#Name: Category, dtype: int64

le = LabelEncoder()
le.fit(filled_nan['Category'])
enc = le.transform(filled_nan['Category'])
filled_nan['Category'] = enc
# le.inverse_transform([0, 1])
#Out[32]: array(['GM', 'SM'], dtype=object)

ohe = OneHotEncoder()
# Converts 1D array into 2D array with rows and columns, as many sklearn
# estimators need 2D arrays and can't work with 1D arrays
reshaped_array = filled_nan['taxon'].to_numpy().reshape(-1,1)
ohe.fit(reshaped_array)
# Without .toarray(), produces a scipy sparse matrix type, but with
# toarray(), produces a np array which is what I want
ohe_values = ohe.transform(reshaped_array).toarray()
#ohe.get_feature_names()
#Out[65]: 
#array(['x0_angiosperm', 'x0_embryophyte', 'x0_eudicot',
#       'x0_viridiplantae'], dtype=object)

names = [name.split('_')[1] for name in ohe.get_feature_names()]
ohe_values_df = pd.DataFrame(data=ohe_values, columns=names, 
                             index=filled_nan.index)
filled_nan_cont = filled_nan.loc[:, 'mean_exp':'OG_size']
filled_nan_cat =  filled_nan.loc[:, 'single_copy':'tandem_dup']
df_GMSM_all = pd.concat(
        [filled_nan_cont, ohe_values_df, filled_nan_cat, 
         filled_nan.loc[:, 'Category']],
        axis=1, sort=False)

df_GMSM_all.index.name = 'Genes'
df_GMSM_all.to_csv('proc_PNAS_data_ML.csv', sep='\t')
