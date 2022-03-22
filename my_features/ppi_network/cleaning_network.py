# -*- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong
From the Biogrid species specific databases, select the arabidopsis one and only select PPIs where
the organism for both proteins is arabidopsis, and where their interaction is protein (there's also
genetic interactions)
"""

import pandas as pd

# Loading complete biogrid database, all species
FILE = './BIOGRID-ORGANISM-4.0.189.tab3/' + \
       'BIOGRID-ORGANISM-Arabidopsis_thaliana_Columbia-4.0.189.tab3.txt'
OUTPUT = 'ath_ppi.txt'

df = pd.read_csv(FILE, sep='\t')
m1 = df['Organism Name Interactor A'].str.contains('Arabidopsis', regex=False)
m2 = df['Organism Name Interactor B'].str.contains('Arabidopsis', regex=False)

ath_only = df.loc[m1 & m2, :]
'''
>>> ath_only['Organism Name Interactor A'].unique()
array(['Arabidopsis thaliana (Columbia)'], dtype=object)
>>> ath_only['Organism Name Interactor B'].unique()
array(['Arabidopsis thaliana (Columbia)'], dtype=object)
'''
ath_only = ath_only.loc[ath_only['Experimental System Type'] == 'physical', :]
ath_only = ath_only.set_index('#BioGRID Interaction ID')
ath_only.to_csv(OUTPUT, sep='\t')

