# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:21:17 2019

@author: weixiong001

Finds lca for each gene, and creates columns corresponding to each taxon and 
uses 1 and 0 to see which gene belongs to which taxon. 
"""
'''
bdi: Brachypodium distachyon -> monocot
tae: Triticum aestivum -> monocot
spo: Spirodela polyrhiza -> monocot
zosmarina: Zostera marina -> monocot
osa: Oryza sativa -> monocot
zma: Zea mays -> monocot

stu: Solanum tuberosumv -> eudicot
sly: Solanum lycopersicum -> eudicot
aly: Arabidopsis lyrata -> eudicot
ath: Arabidopsis thaliana -> eudicot
egr: Eucalyptus grandis -> eudicot
mdo: Malus domestica -> eudicot
mtr: Medicago truncatula -> eudicot
gma: Glycine max -> eudicot
ptr: Populus trichocarpa -> eudicot
vvi: Vitis vinifera -> eudicot

atr: Amborella trichopoda -> angiosperm
pab: Picea abies -> embryophyte
smo: Selaginella moellendorffii -> embryophyte
mpo: Marchantia polymorpha -> bryophyte
ppa: Physcomitrella patens -> bryophyte
cre: Chlamydomonas reinhardtii -> chlorophyte
mco: Micromonas comoda -> chlorophyte

Finds the taxon of each species, then uses it to create a dataframe containg
gene ID and LCA for each gene ID (separated into one column per taxon).
'''

import pandas as pd
import math

# Dictionary showing lineage, to be used to find LCA
taxon_rs = {
        'bdi': 'monocot',
        'osa': 'monocot',
        'tae': 'monocot',
        'spo': 'monocot',
        'zma': 'monocot',
        'zosmarina': 'monocot',
        
        'stu': 'eudicot',
        'sly': 'eudicot',
        'aly': 'eudicot',
        'ath': 'eudicot',
        'egr': 'eudicot',        
        'mdo': 'eudicot',
        'mtr': 'eudicot',
        'gma': 'eudicot',
        'ptr': 'eudicot',
        'vvi': 'eudicot',         
        
        'atr': 'angiosperm',
        'pab': 'embryophyte',
        'smo': 'embryophyte',
        'mpo': 'bryophyte',
        'ppa': 'bryophyte',
        'cre': 'chlorophyte',
        'mco': 'chlorophyte',

        'monocot': 'angiosperm',
        'eudicot': 'angiosperm',
        'angiosperm': 'embryophyte',
        'bryophyte': 'embryophyte',
        'chlorophyte': 'viridiplantae',
        'embryophyte': 'viridiplantae',        
        }

# Used in later part of script to create columns with these names
taxon_list = ['monocot', 'eudicot', 'angiosperm', 'bryophyte', 'embryophyte', 
             'chlorophyte', 'viridiplantae']

###############################################################################
# Code to find lca for a given group of genes
# Obtained this code from, "advanced_python_for_biologists", chapter 2
# recursion and trees

# Get all ancestor taxa for a given taxon
def get_ancestors_rec(taxon):
	if taxon == 'viridiplantae':
		return [taxon]
	else:
		parent = taxon_rs.get(taxon)
		parent_ancestors = get_ancestors_rec(parent) 
		return [parent] + parent_ancestors
   
# Get lca for 2 taxa
def get_lca(taxon1, taxon2): 
    taxon1_ancestors = [taxon1] + get_ancestors_rec(taxon1) 
    for taxon in [taxon2] + get_ancestors_rec(taxon2): 
        if taxon in taxon1_ancestors: 
            return taxon 

# Get lca for a list of taxon
def get_lca_list_rec(taxa):

    if len(taxa) == 1:
        return taxon_rs.get(taxa[0])

    if len(taxa) == 2: 
        return get_lca(taxa[0], taxa[1]) 
    else: 
        taxon1 = taxa.pop() 
        taxon2 = get_lca_list_rec(taxa) 
        return get_lca(taxon1, taxon2)
###############################################################################  

###############################################################################
# This section replaces orthogroup names, with lca, hence each group of genes
# in an orthogroup, now corresponds to its lca
orthogrps_df = pd.read_csv('../gene_families/Orthogroups_edited161019.tsv',
                           sep='\t', index_col=0)

rename_cols = {name: name.split('_')[0] for name in orthogrps_df.columns}
new_og_df = orthogrps_df.rename(columns=rename_cols)

# Replace genes in orthogroups with species in orthogroups
for name in new_og_df.columns:
    mask = ~new_og_df[name].isna()
    new_og_df[name][mask] = name

og_lcas = {}
for og in new_og_df.index:
    all_species = new_og_df.loc[og]
    as_edit = all_species.dropna()
    as_edit = list(as_edit)
    lca = get_lca_list_rec(as_edit)
    if og not in og_lcas:
        og_lcas[og] = lca
    else:
        print('Error, duplicated orthogroup detected')
        break
    
lca_df = orthogrps_df.rename(index=og_lcas)
# Only gets Ath genes with its lca
ath_genes_lca = lca_df['ath_modified'].dropna()
###############################################################################
# Creates the dataframe which contains the various taxa, and shows which of
# them is the lca for each gene

# Converts lca -> genes mapping from above, to gene -> lca mapping
genes_taxon_dict = {}
for taxon in set(ath_genes_lca.index):
    taxon_genes = ath_genes_lca.loc[taxon].str.cat(sep=' ')
    taxon_genes = taxon_genes.split()
    for gene in taxon_genes:
        if gene not in genes_taxon_dict:
            genes_taxon_dict[gene] = taxon
        else:
            print('Error, gene already exist')
            break

# Creates partial_df, which contains the various taxa from taxon_list above,
# and inserts values (1,0) to show the lca of each gene
genes_taxon_df = pd.DataFrame.from_dict(genes_taxon_dict, orient='index')
genes_taxon_df.rename(columns={0: 'master'}, inplace=True)
newlist = ['master'] + taxon_list
partial_df = genes_taxon_df.reindex(columns=newlist, fill_value=0)

for index, row in partial_df.iterrows():
    tx = partial_df.loc[index, 'master']
    partial_df.loc[index, tx] = 1
    
del partial_df['master']

# This checks to make sure there's only one 1 in each row
#(partial_df.sum(axis=1) == 1).all()
#Out[396]: True

# partial_df is the correct df to use, so the name is misleading as no other
# processing is needed
partial_df.index.name = 'genes'
partial_df.to_csv('genes_LCA.tsv', sep='\t')
