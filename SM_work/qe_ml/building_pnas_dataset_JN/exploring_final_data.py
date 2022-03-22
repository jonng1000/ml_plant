# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:13:24 2019

@author: weixiong
"""

import numpy as np
import pandas as pd

final_dataset = pd.read_csv("combined_data_II.txt", sep='\t', index_col=0)

# If I drop rows with NA, only 12 genes left.
# If I drop columns with NA, no features left.
# =============================================================================
# final_dataset.dropna().shape
# Out[201]: (12, 4954)
# 
# final_dataset.dropna(axis=1).shape
# Out[202]: (5251, 0)
# =============================================================================

total_values = final_dataset.shape[0] * final_dataset.shape[1]  # 26013454
non_NA_values = final_dataset.count().sum()  # 22067637
NA_values = total_values - non_NA_values  # 3945817
prop_NAs = NA_values/total_values * 100  # 15.16837018259859%
