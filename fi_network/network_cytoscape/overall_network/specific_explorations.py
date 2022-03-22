# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:20:06 2021

@author: weixiong001

Just basic exploration of 2 features related to GO term GO:0000502
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

FILE = 'D:/GoogleDrive/machine_learning/ml_go_workflow/ml_dataset_dc.txt'
FIG = 'scatter_GO0000502.png'

df = pd.read_csv(FILE, sep='\t', index_col=0)

go_GO_0000502 = df.loc[:, ['ppi_cluster_size', 'agn_cluster_size', 'go_GO:0000502']]
'''
go_GO_0000502['go_GO:0000502'].isna().any()
Out[15]: False
'''
go_GO_0000502 = go_GO_0000502.fillna(go_GO_0000502.mean())

g = sns.scatterplot(x='ppi_cluster_size', y='agn_cluster_size',
                    data=go_GO_0000502.loc[go_GO_0000502['go_GO:0000502'] == 0, :], alpha=0.25)
sns.scatterplot(x='ppi_cluster_size', y='agn_cluster_size',
                data=go_GO_0000502.loc[go_GO_0000502['go_GO:0000502'] == 1, :], 
                alpha=1, ax=g)
g.figure.savefig(FIG)
plt.close()

sel_502 = go_GO_0000502.loc[go_GO_0000502['go_GO:0000502'] == 1, :]
'''
# Just exploring
sel_502['ppi_cluster_size'].value_counts()
Out[45]: 
917.000000    35
41.000000      4
31.000000      2
47.000000      2
8.000000       2
81.000000      2
2.000000       2
11.000000      2
135.960008     2
4.000000       1
Name: ppi_cluster_size, dtype: int64

sel_502['agn_cluster_size'].value_counts()
Out[46]: 
93.0     50
24.0      2
493.0     1
335.0     1
Name: agn_cluster_size, dtype: int64

sel_502.shape
Out[48]: (54, 3)
'''

go_GO_00151712 = df.loc[:, ['tmh_counts', 'cid_cluster_id_97', 'go_GO:0015171']]
'''
go_GO_00151712['go_GO:0015171'].isna().any()
Out[15]: False

go_GO_00151712['cid_cluster_id_97'].isna().any()
Out[52]: False
'''
go_GO_00151712 = go_GO_00151712.fillna(go_GO_00151712.mean())

g = sns.scatterplot(x='tmh_counts', y='cid_cluster_id_97',
                    data=go_GO_00151712.loc[go_GO_00151712['go_GO:0015171'] == 0, :], alpha=0.25)
sns.scatterplot(x='tmh_counts', y='cid_cluster_id_97',
                data=go_GO_00151712.loc[go_GO_00151712['go_GO:0015171'] == 1, :], 
                alpha=1, ax=g)
g.figure.savefig(FIG)
plt.close()

sel_712 = go_GO_00151712.loc[go_GO_00151712['go_GO:0015171'] == 1, :]

'''
sel_712.shape
Out[59]: (33, 3)

sel_712['tmh_counts'].value_counts()
Out[60]: 
10.000000    10
11.000000     6
9.000000      6
3.106506      5
14.000000     2
15.000000     1
13.000000     1
2.000000      1
1.000000      1
Name: tmh_counts, dtype: int64

sel_712['cid_cluster_id_97'].value_counts()
Out[61]: 
0    31
1     2
Name: cid_cluster_id_97, dtype: int64
'''