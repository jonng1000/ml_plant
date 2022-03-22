# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:03:33 2019

@author: weixiong001
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("combined_data_ML.csv", sep="\t", index_col=0)

#df['Category'].value_counts()
#Out[66]: 
#no_label    26547
#GM           1488
#SM            115
#Name: Category, dtype: int64

#df.shape
#Out[69]: (28150, 11)

#df.isna().sum()
#Out[70]: 
#mean_exp        768
#median_exp      768
#max_exp         768
#min_exp         768
#var_exp         768
#var_median     6794
#OG_size        2376
#taxon          2376
#single_copy    2376
#tandem_dup      495
#Category          0
#dtype: int64

df_no_nan_rows = df.dropna()

#df_no_nan_rows['Category'].value_counts()
#Out[77]: 
#no_label    19409
#GM           1436
#SM            106
#Name: Category, dtype: int64

#df_no_nan_rows.isna().any().any()
#Out[80]: False

fig, ax = plt.subplots(figsize=(12,12))
sns.heatmap(df_no_nan_rows.corr(method='pearson'), ax=ax)
plt.savefig("heatmap_corr.png")

# Need to use .copy() here, to suppress warning about changing values
# when view/copy returned object is ambigous
df_GMSM = df_no_nan_rows[df_no_nan_rows['Category'] != 'no_label'].copy()

#df_GMSM['Category'].value_counts()
#Out[23]: 
#GM    1436
#SM     106
#Name: Category, dtype: int64

#df_GMSM.dtypes
#Out[24]: 
#mean_exp       float64
#median_exp     float64
#max_exp        float64
#min_exp        float64
#var_exp        float64
#var_median     float64
#OG_size        float64
#taxon           object
#single_copy    float64
#tandem_dup     float64
#Category        object
#dtype: object

le = LabelEncoder()
le.fit(df_GMSM['Category'])
enc = le.transform(df_GMSM['Category'])
df_GMSM['Category'] = enc

# le.inverse_transform([0, 1])
#Out[32]: array(['GM', 'SM'], dtype=object)

ohe = OneHotEncoder()
# Converts 1D array into 2D array with rows and columns, as many sklearn
# estimators need 2D arrays and can't work with 1D arrays
reshaped_array = df_GMSM['taxon'].to_numpy().reshape(-1,1)
ohe.fit(df_GMSM['taxon'].to_numpy().reshape(-1,1))
# Without .toarray(), produces a scipy sparse matrix type, but with
# toarray(), produces a np array which is what I want
ohe_values = ohe.transform(reshaped_array).toarray()

#ohe.get_feature_names()
#Out[65]: 
#array(['x0_angiosperm', 'x0_embryophyte', 'x0_eudicot',
#       'x0_viridiplantae'], dtype=object)

names = [name.split('_')[1] for name in ohe.get_feature_names()]
ohe_values_df = pd.DataFrame(data=ohe_values, columns=names, 
                             index=df_GMSM.index)
df_GMSM_cont = df_GMSM.loc[:, 'mean_exp':'OG_size']
df_GMSM_cat =  df_GMSM.loc[:, 'single_copy':'tandem_dup']
df_GMSM_cat_all = pd.concat([df_GMSM_cat, ohe_values_df, 
                             df_GMSM.loc[:, 'Category']], axis=1, sort=False)

processed = pd.concat([df_GMSM_cont, df_GMSM_cat_all], axis=1, sort=False)
processed.index.name = 'Genes'
processed.to_csv('processed_data_ML.csv', sep='\t')
