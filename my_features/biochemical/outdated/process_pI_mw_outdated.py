# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:43:18 2021

@author: weixiong001

Used to look at pI and mw calculations from web based IPC2, but too little proteins, so discard
"""

import pandas as pd

FILE = 'result.csv'
OUTPUT = 'ath_pI_mw.txt'

df = pd.read_csv(FILE, sep=',', index_col=0)
"""
selected = df.loc[:, [' molecular_weight', ' Avg_pI']]
#renamed.to_csv(OUTPUT, sep='\t')
temp = selected.index.str.split('GN=')
expaned_temp = pd.DataFrame(temp.values.tolist())
temp2 = expaned_temp.loc[:, 1].str.split(' ')
expaned_temp2 = pd.DataFrame(temp2.values.tolist())
gene_names = expaned_temp2.loc[:, 0]
gene_names_caps = gene_names.str.upper()

temp_set = set([x[:4] for x in gene_names_caps])
'''
gene_names_caps[gene_names_caps.str.contains(r"AT\d[GMC]\d{5}")]
Out[94]: 
3        AT1G52565
4        AT4G21865
5        AT1G23465
6        AT4G14145
7        AT3G21490
   
33420    AT2G38900
33424    AT1G78730
33430    AT2G16940
33432    AT2G29290
33439    AT2G43230
Name: 0, Length: 14795, dtype: object
'''
"""
#Only has about 14k genes in the AT*G/M/C format so shall not use this, use
# Used the author's calculator 2.0 to calculate for mine