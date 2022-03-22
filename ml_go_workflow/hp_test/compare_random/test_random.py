# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 14:51:14 2021

@author: weixiong001

Just testing to make sure that my random shuffling of features works
"""

import pandas as pd

FILE = 'ml_dataset_dc.txt'

data = pd.read_csv(FILE, sep='\t', index_col=0)

data2 = data.apply(lambda x: x.sample(frac=1).values)


df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
                   'num_wings': [2, 0, 0, 0],
                   'num_specimen_seen': [10, 2, 1, 8]},
                      index=['falcon', 'dog', 'spider', 'fish'])

'''
data['tpm_max']
Out[6]: 
Gene
ATCG00500    114.225174
ATCG00510     11.527975
ATCG00280    598.933800
ATCG00890     13.217823
ATCG01250     13.217823
   
AT5G66558           NaN
AT5G66562           NaN
ATCG00370           NaN
ATMG01380           NaN
ATMG01390           NaN
Name: tpm_max, Length: 31522, dtype: float64

data2 = data.apply(lambda x: x.sample(frac=1).values)

data2['tpm_max']
Out[8]: 
Gene
ATCG00500    92.629875
ATCG00510    65.872850
ATCG00280    34.661415
ATCG00890    18.625422
ATCG01250    44.781857
   
AT5G66558     5.786258
AT5G66562     6.944565
ATCG00370          NaN
ATMG01380    15.524393
ATMG01390    10.173770
Name: tpm_max, Length: 31522, dtype: float64
'''

'''
Out[11]: 
        num_legs  num_wings  num_specimen_seen
falcon         2          2                 10
spider         8          0                  1

df
Out[12]: 
        num_legs  num_wings  num_specimen_seen
falcon         2          2                 10
dog            4          0                  2
spider         8          0                  1
fish           0          0                  8

df.sample(frac=0.5, axis=0)
Out[13]: 
        num_legs  num_wings  num_specimen_seen
fish           0          0                  8
falcon         2          2                 10

df.sample(frac=0.5, axis=1)
Out[14]: 
        num_wings  num_legs
falcon          2         2
dog             0         4
spider          0         8
fish            0         0

df
Out[15]: 
        num_legs  num_wings  num_specimen_seen
falcon         2          2                 10
dog            4          0                  2
spider         8          0                  1
fish           0          0                  8

df2 = df.apply(lambda x: x.sample(frac=1).values)

df2
Out[17]: 
        num_legs  num_wings  num_specimen_seen
falcon         8          0                  8
dog            0          2                  2
spider         2          0                  1
fish           4          0                 10
'''
