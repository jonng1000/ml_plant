# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:24:54 2020

@author: weixiong001

Plotting graph to see how my results look like - draft script so can ignore
"""

import numpy as np
import pandas as pd
#import seaborn as sns
#from matplotlib import pyplot as plt

FILE = 'dge_1HE_edited.txt'

df = pd.read_csv(FILE, sep="\t", index_col=0)

'''
# Checking df
np.unique(df.to_numpy(), return_counts=True)
Out[6]: (array([0, 1], dtype=int64), array([10849093,   678747], dtype=int64))

len(df.columns) * len(df.index)
Out[15]: 11527840

10849093 + 678747
Out[16]: 11527840

678747/(len(df.columns) * len(df.index)) * 100
Out[14]: 5.887894002692612
'''

up_array = df.columns[df.columns.str.contains('up')]
down_array = df.columns[df.columns.str.contains('down')]

up_df = df.loc[:, up_array]
down_df = df.loc[:, down_array]

'''
# Checking df
np.unique(up_df.to_numpy(), return_counts=True)
Out[11]: (array([0, 1], dtype=int64), array([5426440,  337480], dtype=int64))

len(up_df.columns) * len(up_df.index)
Out[12]: 5763920

5426440 + 337480
Out[16]: 5763920

337480/(len(up_df.columns) * len(up_df.index)) * 100
Out[15]: 5.855043095671002
'''

up_long = pd.melt(up_df)
'''
# Should have used pd.melt() instead of the above
up_long['value'].value_counts()
Out[18]: 
0    5426440
1     337480
Name: value, dtype: int64
'''
up_long['value'].value_counts().plot.bar()

'''
# Checking df
np.unique(down_df.to_numpy(), return_counts=True)
Out[11]: (array([0, 1], dtype=int64), array([5422653,  341267], dtype=int64))

len(down_df.columns) * len(down_df.index)
Out[12]: 5763920

5422653 + 341267
Out[16]: 5763920

341267/(len(down_df.columns) * len(down_df.index)) * 100
Out[15]: 5.920744909714222
'''

down_long = pd.melt(down_df)
'''
# Should have used pd.melt() instead of the above
down_long['value'].value_counts()
Out[23]: 
0    5422653
1     341267
Name: value, dtype: int64
'''
down_long['value'].value_counts().plot.bar()
