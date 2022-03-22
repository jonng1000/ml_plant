# -*- coding: utf-8 -*-
"""
Created on 230620

@author: weixiong
Sanity check to ensure that all RNA-seq data have been downloaded and properly
processed by kallisto
"""

import pandas as pd
import os

FILE = 'rna_seq_dl.txt'
KAL_FOLDER = './kal_output'

df = pd.read_csv(FILE, sep='\t', index_col=0)
'''
# Number of unique run IDs
len(df['Run'].drop_duplicates())
Out[4]: 1370
'''
processed_kal = set(os.listdir(path=KAL_FOLDER))
'''
# No duplicates in kallisto output folders
>>> len(processed_kal) == len(os.listdir(path=KAL_FOLDER))
True
# Number of processed kallisto folders after RNA-seq download
>>> len(processed_kal)
1367
>>> len(set(df['Run']))
1370

# After downloading the 3 missing RNA-seq data
>>> len(processed_kal)
1370
'''
processed_kal = {i.split('_')[0] for i in processed_kal}
'''
# Shows missing data files, and that all folders in the kallisto output
# directory is found in the list of RNA-seq data to download
>>> set(df['Run']) - processed_kal
{'SRR1564469', 'SRR3932359', 'SRR3932358'}
>>> processed_kal - set(df['Run'])
set()

# After downloading the 3 missing RNA-seq data
# All RNA-seq data is my list of data to download, has been downloaded
>>> set(df['Run']) - processed_kal
set()
>>> processed_kal - set(df['Run'])
set()
>>> set(df['Run']) == processed_kal
True
'''
