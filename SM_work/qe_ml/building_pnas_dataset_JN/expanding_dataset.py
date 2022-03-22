# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:00:15 2019

@author: weixiong001

Designed to use a dataset (semi-finished) and expand upon it to build a final
one
"""

import numpy as np
import pandas as pd

dataset = pd.read_csv("d1s1.txt", sep='\t', index_col=0)

# Below code shows output of orginal values from data set
# Need to replace none with NaN and remove  Seconday and Non-secondary 
# metabolism pathway genes from dataset
# =============================================================================
# dataset['AraCyc annotation'].value_counts(dropna=False)
# Out[9]: 
# none                                             2933
# Non-secondary metabolism pathway                 1306
# Secondary metabolism pathway                      423
# Seconday and Non-secondary metabolism pathway     264
# NaN                                                18
# Name: AraCyc annotation, dtype: int64
# =============================================================================

dataset = dataset.replace('none', np.nan)
# =============================================================================
# dataset['AraCyc annotation'].value_counts(dropna=False)
# Out[20]: 
# NaN                                              2951
# Non-secondary metabolism pathway                 1306
# Secondary metabolism pathway                      423
# Seconday and Non-secondary metabolism pathway     264
# Name: AraCyc annotation, dtype: int64
# =============================================================================
pathways_set = dataset['AraCyc pathways'].value_counts(dropna=False)
# Shows that there all undefined vlaues in 'AraCyc pathways' are NaN, but
# original column probably already has this characteristic
# =============================================================================
# pathways_set.tail()
# Out[25]: 
# PWY-4041|&gamma;-glutamyl cycle; PWY-6745|phytochelatins biosynthesis; 
# PWYQT-4432|glutathione degradation; PWY-6842|glutathione-mediated 
# detoxification II      1
# PWY-6762|salicylate glucosides biosynthesis IV; PWY-6624|salicylate glucosides
#  biosynthesis III; PWY-7468|benzoyl-&beta;-<i>D</i>-glucopyranose 
#  biosynthesis    1
# .
# .
# .
# Name: AraCyc pathways, dtype: int64
# 
# pathways_set.head()
# Out[26]: 
# NaN                                                2172
# PWY-1081|homogalacturonan degradation                76
# LIPAS-PWY|triacylglycerol degradation                65
# PWY-6842|glutathione-mediated detoxification II      51
# PWY-5992|thalianol and derivatives biosynthesis      37
# Name: AraCyc pathways, dtype: int64
# =============================================================================

list_pathways = dataset['AraCyc pathways'].apply(lambda x: np.nan if pd.isna(x) else x.split("; "))
pathways = []
for row in list_pathways:
    #row = [a_pathway.strip() for a_pathway in row]
    if pd.isna(pd.Series(row)).any():
        continue
    else:
        for a_pathway in row:
            a_pathway = a_pathway.strip()
            if a_pathway not in pathways:
                pathways.append(a_pathway)
                
for pathway in pathways:
    # shape is (4944, 593)
    dataset[pathway] = dataset['AraCyc pathways'].str.contains(pathway, regex=False).astype(float)
edited = dataset.drop(columns=['AraCyc pathways'])

# shape is (5239, 4362)
dataset2 = pd.read_csv("combined_data.txt", sep='\t', index_col=0)
# shape is (52551, 4954)
final_dataset = dataset2.join(edited, how='outer')
final_dataset.index.name = 'Gene'
final_dataset.to_csv("combined_data_II.txt", sep='\t', na_rep='NA')


