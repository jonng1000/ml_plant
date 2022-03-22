# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:21:35 2019

@author: weixiong

goa_uniprot_all_noiea.gaf cant be read with biopython's .gaf parser as its
format is weird, so use this script to filter it
"""

import pandas as pd
import csv

expt_codes = {'EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP'}
with open('all_children_GO0019748.csv', newline='') as csvfile1,\
    open('all_children_GO0044238.csv',  newline='') as csvfile2:
        reader1 = csv.reader(csvfile1, delimiter='\t')
        reader2 = csv.reader(csvfile2, delimiter='\t')
        for secondary_GOs in reader1:
            pass
        for primary_GOs in reader2:
            pass


df = pd.read_csv('.\cannot_read_gaf\goa_uniprot_all_noiea.gaf.gz', 
                 compression='gzip', header=None, sep='\t')
df.rename(columns={2:'Gene', 3:'Annotation_qualifier', 4:'GO_class', 
                   6: 'Evidence', 12:'Organism'}, inplace=True)
df = df[df['Annotation_qualifier'] != 'NOT']
df = df[df['Evidence'].isin(expt_codes)]
df = df[df['GO_class'].isin(primary_GOs + secondary_GOs)]
df = df[['Gene','GO_class', 'Evidence', 'Organism']]
df.reset_index(drop=True, inplace=True)

df.to_csv('goa_noiea_filtered.csv', sep='\t', na_rep='NA', index=False)
