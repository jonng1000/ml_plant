# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:13:36 2019

@author: weixiong001
"""

import pandas as pd
import os
import csv
from Bio import Entrez
from itertools import groupby

#GO_data1 = 'Viridiplantae_priGO.txt'
#GO_data2 = 'Viridiplantae_secGO.txt'

def count_species(GO_data):
    df = pd.read_csv(GO_data, sep='\t', header=None)
    df.rename(columns={2:'Gene', 3:'Annotation_qualifier', 4:'GO_class', 
                       11:'Type', 12:'Organism'}, inplace=True)    
    df = df[df['Annotation_qualifier'] != 'not']
    df = df[df['Type'].isin(['protein', 'gene', 'gene_product'])]
    df = df[['Gene', 'Organism']]
    df = df.drop_duplicates(subset='Gene', keep='first')
    counts = df['Organism'].value_counts()
    return counts

def SM_GM_counts_species(countsGM, countsSM):
    counts1 = countsGM.rename('GM') 
    counts2 = countsSM.rename('SM')
    counts_df = pd.concat([counts1, counts2], axis=1, sort=False)
    counts_df.sort_values('SM', inplace=True, ascending=False)
    return counts_df

def rename_df(GM_SM_c):
    # convert to function
    taxon_numbers = [taxon.split(':')[1] for taxon in GM_SM_c.index]
    Entrez.email = 'weixiong001@ntu.edu.sg'  # Put your email here
    handle = Entrez.efetch('taxonomy', id=taxon_numbers, rettype='text')
    response = Entrez.read(handle)
    
    map_ids_names = {}
    for entry in response:
        sci_name = entry.get('ScientificName')
        taxon_id = entry.get('TaxId')
        ncbi_id_amigo = 'NCBITaxon:' + taxon_id
        if ncbi_id_amigo not in map_ids_names:
            map_ids_names[ncbi_id_amigo] = str(sci_name)
        else:
            print(ncbi_id_amigo,'already found, duplicate ID detected')
            
    GM_SM_c.rename(index=map_ids_names, inplace=True)
    return GM_SM_c

dl_data = [file for file in os.listdir() if file.endswith('GO.txt')]
# Important for groupby to work
# priGo file will always be before secGO file since list is sorted
dl_data.sort()
# priGO file still before secGO since groupby function does not change order
grouped_data = [ list(j) for i,j in 
                groupby(dl_data, lambda x: x.split('_')[0])]

# Doing the actuall parsing     
for taxon in grouped_data:
    # This depends on order of grouped)data being correct, refer to comments
    # in the anobe dl_data sorting for more info
    GM_c = count_species(taxon[0])
    SM_c = count_species(taxon[1])
    GM_SM_df = SM_GM_counts_species(GM_c, SM_c)
    GM_SM_rename_df = rename_df(GM_SM_df)
    filename_to_save = taxon[0].split('_')[0] + '_counts.csv'
    GM_SM_rename_df.to_csv(filename_to_save, sep='\t', na_rep='NA')



