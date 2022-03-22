# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:31:25 2021

@author: weixiong001

Combing all the scores files and calculating the time taken for all the ml 
models used
"""

import os
import re
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

OUTPUT = 'compiled_times.txt'

all_df = []
for a_file in os.listdir('./'):
    result = re.search('GO.{8}', a_file)
    
    # Checks for GO scores file, only these files will give a result
    # all others will return None
    if result == None:
        continue
    temp_go = result.group()
    go_term = temp_go.replace('_', ':')
    data = pd.read_csv(a_file, sep='\t', index_col=0)
    data.insert(0, 'GO_class', go_term)
    
    # Logr file has both logr and lsv values, but only want logr values,
    # as lsv values aren't verified to be true, and I have a separate lsv file
    # with verified values, hence will remove lsv values from this logr file
    if a_file.startswith('logr'):
        data = data.loc[data['model_name'].str.contains('logr'), :]
        
    all_df.append(data)

# Combining all the dfs and processing them into the final file
combined = pd.concat(all_df)
combined['time_start'] = pd.to_datetime(combined['time_start'], dayfirst=True)
combined['time_end'] = pd.to_datetime(combined['time_end'], dayfirst=True)
combined['time_taken'] = combined['time_end'] - combined['time_start']
combined['time_taken_(s)'] = combined['time_taken'].astype('timedelta64[s]')
combined['time_taken_(min)'] = combined['time_taken'].astype('timedelta64[m]')
combined['time_taken_(h)'] = combined['time_taken'].astype('timedelta64[m]')

selected = combined.loc[:, ['GO_class', 'model_name', 'time_taken_(s)', 
                            'time_taken_(min)', 'time_taken_(h)']]
# Saving this to file, to show that there's not always error bars due to time
# being the same for some models
selected.to_csv(OUTPUT, sep='\t')
