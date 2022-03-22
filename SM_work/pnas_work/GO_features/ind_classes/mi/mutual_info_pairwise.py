"""
Calculates mutual information (mi)

Note: Running the mi function on a large dataset takes 5min, but running it
repeated on several large datasets also takes 5min
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import mutual_info_regression
from datetime import datetime

#################################################################################
# Calculating mi from my golgi dataset
#################################################################################
FILE = 'Golgi_apparatus_GO.txt'
MI_FILE = 'mi_golgi_pairwise.txt'
CLASS_LABELS = 'AraCyc annotation'
df = pd.read_csv(FILE, sep="\t", index_col=0)

pos = df[CLASS_LABELS].value_counts().idxmin()
neg = df[CLASS_LABELS].value_counts().idxmax()
df.loc[:, 'AraCyc annotation'].replace([pos, neg], [1, 0], inplace=True)
y = df['AraCyc annotation']

print('Script started', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
#################################################################################
# Creating list discrete features based on work above, then calculate mi
# through various methods and compare the result
#################################################################################
discrete_var = ['Gene family size', 'Co-localized SM gene clusters (5 genes)', 'Co-localized SM gene clusters (10 genes)', 'Co-localized PM gene clusters (5 genes)', 'Co-localized PM gene clusters (10 genes)', 'abiotic-shoot up-regulation',  'abiotic-shoot down-regulation', 'abiotic-shoot up/down regulation', 'abiotic-root up-regulation', 'abiotic-root down-regulation', 'abiotic-root up/down regulation', 'biotic up-regulation', 'biotic down-regulation', 'biotic up/down regulation', 'hormone up-regulation', 'hormone down-regulation', 'hormone up/down regulation', 'Co-expressed cluster at k=2000, develop', 'Number of domains',  'Amino acid length', 'Aranet gene-interactions']
discrete_var.extend(list(df.select_dtypes(include=['int64']).columns))

man_discrete_df = df.loc[:, discrete_var]
man_cont_df = df.drop(columns=discrete_var)

set_discrete = set(discrete_var)
lst_series = []
c = 0
for feature in df.columns:
    y = df[feature]
    if feature in set_discrete:
        man_discrete_mi_array =  mutual_info_classif(man_discrete_df, y,
                                                     discrete_features=True)
        man_cont_mi_array =  mutual_info_classif(man_cont_df, y,
                                                 discrete_features=False)
        man_cont_mi = pd.Series(man_cont_mi_array, index=man_cont_df.columns)
        man_discrete_mi = pd.Series(man_discrete_mi_array,
                                    index=man_discrete_df.columns)
        man_dtypes_mi = man_cont_mi.append(man_discrete_mi)
        lst_series.append(man_dtypes_mi)
    else:        
        man_discrete_mi_array =  mutual_info_regression(man_discrete_df, y,
                                                     discrete_features=True)
        man_cont_mi_array =  mutual_info_regression(man_cont_df, y,
                                                 discrete_features=False)
        man_cont_mi = pd.Series(man_cont_mi_array, index=man_cont_df.columns)
        man_discrete_mi = pd.Series(man_discrete_mi_array,
                                    index=man_discrete_df.columns)
        man_dtypes_mi = man_cont_mi.append(man_discrete_mi)
        lst_series.append(man_dtypes_mi)
    c += 1
    print('feature', c, feature, 'done', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

mi_df = pd.concat(lst_series, axis=1)
mi_df.columns = df.columns[:100]
mi_df.index.name = 'Features'
mi_df.to_csv(MI_FILE, sep='\t')
