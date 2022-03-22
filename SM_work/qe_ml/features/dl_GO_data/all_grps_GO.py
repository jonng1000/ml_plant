# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:13:36 2019

@author: weixiong001

Finds all GM and SM genes in each taxon group
"""

import pandas as pd
import os
import csv

# This function finds unique genes from the downloaded GO file from AmiGO
# Tested this function on bacteria pri GO genes, ~5.7k genes, after
# finding unique genes, its about ~2.6k
def find_unique_genes(GO_data):
    df = pd.read_csv(GO_data, sep='\t', header=None)
    df.rename(columns={2:'Gene', 3:'Annotation_qualifier', 4:'GO_class', 
                       11:'Type', 12:'Organism'}, inplace=True)
    
    df = df[df['Annotation_qualifier'] != 'not']
    df = df[df['Type'].isin(['protein', 'gene', 'gene_product'])]
    unique_genes = set(df['Gene'])
    return unique_genes

# Groupping the GO files into groups based on their overall taxonomic group
dl_data = [file for file in os.listdir() if file.endswith('.txt')]
grouped_dict = {}
for f in dl_data:
    taxon = f.split('_')[0]
    if taxon in grouped_dict:
        grouped_dict[taxon] = grouped_dict[taxon] + [f]
    else:
        grouped_dict[taxon] = [f]
 
# Doing the actuall parsing     
for taxon in grouped_dict:
    if grouped_dict[taxon][0].endswith('priGO.txt'):
        if grouped_dict[taxon][1].endswith('secGO.txt'):
            priGO_genes = find_unique_genes(grouped_dict[taxon][0])
            secGO_genes = find_unique_genes(grouped_dict[taxon][1])
            with open(taxon + '_priGO_genes.txt', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                for gene in priGO_genes:
                    writer.writerow([gene])
            with open(taxon + '_secGO_genes.txt', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                for gene in secGO_genes:
                    writer.writerow([gene])            
        else:
            print('error here!')
            break
    # Assume if case above is always true, rewrite code if needed to take
    # care of else case
    else:
        print('files not in expected order')
        break
