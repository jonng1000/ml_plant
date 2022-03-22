# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

This script takes in OrthoFinder results from Irene, and determines if each
arabidopsis gene has homologs with all other species. 23 species in the
orthogroup file, orthogroup info from Irene's evorepro paper

Homologs are defined as, if an arabidopsis gene and genes from other species,
are in the same orthogroup
"""

import os
import pandas as pd
import csv
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import single_letter_alphabet

FOLDER = './proteomes_EvoRepro/'
FILE = 'Orthogroups.txt'
OUTPUT = 'ath_homologs.txt'

# Creates a dict, mapping each fasta sequence (Irene's orthogroup data) to its
# respective species name
gene_species = {}
for one in os.listdir(FOLDER):
    species_name = one.split('.')[0]
    file_path = FOLDER + one
    with open(file_path) as fasta_f:
        records = SeqIO.parse(fasta_f, 'fasta')
        for record in records:
            # Checking
            if record.id in gene_species:
                print('already seen')
            else:
                gene_species[record.id] = species_name

# Dictionary: connects each arabidopsis gene to its orthogroup
ath_og = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        # Includes test to make sure orthogroup ids are unique
        og = row[0].split(':')[0]
        genes = row[1:]
        ath_genes = [one for one in genes if one.startswith('AT')]
        for gene in ath_genes:
            # Checking
            if gene in ath_og:
                print(gene, 'present')
            else:
                ath_og[gene] = og

ath_letters = [x[:4] for x in ath_og.keys()]
'''
# Shows that I have selected all arabidopsis genes
set(ath_letters)
Out[10]: {'AT1G', 'AT2G', 'AT3G', 'AT4G', 'AT5G', 'ATCG', 'ATMG'}
# Checks to make sure, my arabidopsis genes are unique
len(ath_og.keys())
Out[63]: 27655
len(set(ath_og.keys()))
Out[64]: 27655
'''

# Dictionary: Shows what are the species in each othrogroup
og_species = {}
with open(FILE, newline='') as csvfile:
    csv_read = csv.reader(csvfile, delimiter=' ')
    for row in csv_read:
        og = row[0].split(':')[0]
        genes = row[1:]
        species_set = set()
        for x in genes:
           species_set.add(gene_species[x])
        if og in og_species:
            # Checking
            print(og, 'exist')
        else:
            og_species[og] = species_set
            

# Dictionary: Shows what are the homologous species for each arabidopsis gene
ath_species = {}
for ath_gene in ath_og:
    orth = ath_og[ath_gene]
    homolog_species = og_species[orth]
    ath_species[ath_gene] = list(homolog_species)
    
ath_series = pd.Series(ath_species)
ath_df = ath_series.explode().to_frame()
expanded = pd.get_dummies(ath_df, prefix=['hom'])
expanded.index.name = 'Gene'

homologs_presence = expanded.groupby(['Gene']).sum()
'''
# Dimensions, includes arabidopsis, so need to remove as it doesn't makes sense
# as I am detecting homologs
homologs_presence.shape
Out[138]: (27655, 23)
'''
# Drop the arabidopsis column, as I only want homologs, hence this doesn't
# make sense
dropped = homologs_presence.drop(columns=['hom_Arabidopsis_thaliana'])
ath_homologs = dropped.loc[dropped.sum(axis=1)!=0, :]
ath_homologs.to_csv(OUTPUT, sep='\t')

"""
ath_homologs.shape
Out[150]: (22920, 22)

ath_homologs
Out[28]: 
           hom_Amborella_trichopoda  ...  hom_Zostera_marina
Gene                                 ...                    
AT1G01020                         1  ...                   1
AT1G01030                         1  ...                   1
AT1G01040                         1  ...                   1
AT1G01050                         1  ...                   1
AT1G01060                         1  ...                   1
                            ...  ...                 ...
ATMG01280                         1  ...                   0
ATMG01320                         0  ...                   0
ATMG01330                         0  ...                   0
ATMG01360                         1  ...                   1
ATMG01410                         1  ...                   1

[22920 rows x 22 columns]

ath_homologs.sum()
Out[29]: 
hom_Amborella_trichopoda          20993
hom_Azolla_filiculoides           18180
hom_Brachypodium_distachyon       21103
hom_Chara_braunii                 14074
hom_Chlamydomonas_reinhardtii     12039
hom_Cyanidioschyzon_merolae        7348
hom_Cyanophora_paradoxa            9958
hom_Ginkgo_biloba                 19567
hom_Gnetum_montanum               19803
hom_Klebsormidium_flaccidum       15928
hom_Marchantia_polymorpha         18145
hom_Micromonas_commoda            10712
hom_Oryza_sativa                  21092
hom_Physcomitrium_patens          18280
hom_Picea_abies                   20221
hom_Porphyridium_purpureum         8412
hom_Salvinia_cucullata            18378
hom_Selaginella_moellendorffii    17086
hom_Solanum_lycopersicum          22195
hom_Vitis_vinifera                21330
hom_Zea_mays                      20747
hom_Zostera_marina                20350
dtype: int64
"""
