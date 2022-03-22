# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in the Arabidopsis diurnal gene expression from Marek
and does one hot encoding according to a custom function. Diurnal 
conditions where expression data are obtained from, are one hot encoded.
Amplitude of diurnal variation are also stored here. Diurnal expression is
obtained via JTK script from the literature.
End product is saved to a new file. Edited from process_ath_exp.py
in /mnt/d/GoogleDrive/machine_learning/my_features/data_preprocessing

251120 edit: Has gene ganes with AFFX letters, these are Affy probes
not genes so removed such rows. Script output would be overwitten with
this correction
"""

import pandas as pd
import numpy as np

FILE = 'JTK.Ath_Mat.txt'
OUTPUT = 'edited_Ath_jtk.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
# This two lines may not be always essential, but is written to ensure that the
# df index is standardised in the output file, regardless of index in input
# file
df = df.loc[~df.index.str.startswith('AFF'), :]
df.index = df.index.str.upper()
df.index.name = 'Gene'

selected_df = df.loc[:, ['ADJ.P', 'LAG', 'AMP']].copy()
selected_df.loc[selected_df['ADJ.P'] >= 0.05, 'AMP']
selected_df.loc[selected_df['ADJ.P'] >= 0.05, 'AMP'] = np.nan
selected_df.loc[selected_df['ADJ.P'] >= 0.05, 'LAG'] = np.nan
ohe_diu = pd.get_dummies(selected_df, columns=['LAG'], prefix='dit')
ohe_diu.drop(columns=['ADJ.P'], inplace=True)
ohe_diu.rename(columns={'AMP': 'dia_AMP'}, inplace=True)

ohe_diu.to_csv(OUTPUT, sep='\t', na_rep='NA')
'''
# df dimensions
>>> ohe_diu.shape
(22746, 13)
'''
