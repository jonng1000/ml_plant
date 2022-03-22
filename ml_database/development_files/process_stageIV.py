# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 19:28:47 2022

@author: weixiong001

More processing of data due to Marek's suggestions.
Renaming to give more easily understood names
"""

import pandas as pd

FILE = 'processed_stage3.txt'
AA_FILE = 'single_letter_aa_lookup.txt'
PTM_FILE = 'ptm_lookup.txt'
PFAM_FILE = 'pfam_desc.txt'
OUTPUT = 'processed_stage4.txt'

df = pd.read_csv(FILE, index_col=0 , sep='\t')
df = df.reset_index()

aa_df = pd.read_csv(AA_FILE, header=None , sep='\t')
aa_df.rename(columns={0: 'letter', 1:'name'}, inplace=True)
aa_df['letter'] = aa_df['letter'].str.upper()

ptm_df = pd.read_csv(PTM_FILE, header=None , sep='\t')
ptm_df.rename(columns={0: 'short_form', 1:'ptm'}, inplace=True)

pfam_df = pd.read_csv(PFAM_FILE, index_col=0 , sep='\t')

##############################################################################
# Correcting typos
df.loc[(df['Category'] == 'Homologs in other speceies (hom)') & 
       (df['Feature name'] == 'hom_Ginkbiloba'), 
       'Feature name'] = 'hom_Ginkgo_biloba'

# String is correct
df.loc[(df['Category'] == 'DGE_stress and stimulus (dge)') & 
       (df['Feature name'] == 'dge_E-GEOD-54680_2_down'), 
       'Description']
df.loc[(df['Category'] == 'DGE_stress and stimulus (dge)') & 
       (df['Feature name'] == 'dge_E-GEOD-54680_2_up'), 
       'Description']
df.loc[(df['Category'] == 'DGE_stress and stimulus (dge)') & 
       (df['Feature name'] == 'dge_E-GEOD-54680_4_down'), 
       'Description']
df.loc[(df['Category'] == 'DGE_stress and stimulus (dge)') & 
       (df['Feature name'] == 'dge_E-GEOD-54680_4_up'), 
       'Description']

df.loc[(df['Description'] == 'Whether gene body is methlyated'), 
       'Description'] = 'Whether gene body is methylated'

df.loc[df['Category'] == 'Homologs in other speceies (hom)', 
                       'Category'] = 'Homologs in other species (hom)'

df.loc[df['Category'] == 'Gene expression, diurnal timepoint (dit)', 
       'Description'] = 'Timepoint with maximum diurnal gene expression'
##############################################################################

# Aranet features
df.loc[(df['Category'] == 'Aranet, functional gene network clusters (agi)'), 
       'Description'] = 'Cluser id, genes which belong to the same Aranet cluster, obtained from https://www.inetbio.org/aranet/'
desc = df.loc[df['Category'] == 'Aranet, functional gene network features (agn)', 
              'Description'] 
df.loc[df['Category'] == 'Aranet, functional gene network features (agn)', 
       'Description'] = desc.astype(str) + ', obtained from https://www.inetbio.org/aranet/'


# Gene coexp features
df.loc[(df['Category'] == 'Gene coexpression clusters (cid)'), 
       'Description'] = 'Cluser id, genes which belong to the same gene coexpression cluster, obtained from https://evorepro.sbs.ntu.edu.sg/'
desc = df.loc[df['Category'] == 'Gene coexpression network features (coe)', 
              'Description'] 
df.loc[df['Category'] == 'Gene coexpression network features (coe)', 
       'Description'] = desc.astype(str) + ', obtained from https://evorepro.sbs.ntu.edu.sg/'

# cis-regulatory features
cis_fam = df.loc[(df['Category'] == 'cis-regulatory element families (cif)'), 
                 'Feature name'].str.split('_').str[1]
df.loc[(df['Category'] == 'cis-regulatory element families (cif)'), 
       'Description'] = 'Gene regulation, number of ' + cis_fam.astype(str) + ' cis element families in gene, obtained from AtcisDB at https://agris-knowledgebase.org/downloads.html'

cis_nam = df.loc[(df['Category'] == 'cis-regulatory element names (cin)'), 
                 'Feature name'].str.split('_').str[1]
df.loc[(df['Category'] == 'cis-regulatory element names (cin)'), 
       'Description'] = 'Gene regulation, number of ' + cis_nam.astype(str) + ' cis elements in gene, obtained from AtcisDB at https://agris-knowledgebase.org/downloads.html'
'''
# Outdated
df.loc[(df['Category'] == 'cis-regulatory element families (cif)'), 
       'Description'] = 'Gene regulation, obtained from AtcisDB at https://agris-knowledgebase.org/downloads.html'
df.loc[(df['Category'] == 'cis-regulatory element names (cin)'), 
       'Description'] = 'Gene regulation, obtained from AtcisDB at https://agris-knowledgebase.org/downloads.html'
'''

# Conservation features
df.loc[df['Feature name'] == 'con_Percent identity with putative paralog', 
       'Description'] = 'Maximum percent identity from BLAST to closest paralog, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_Sequence conservation in Fungi (% ID)', 
       'Description'] = 'Protein sequence % identity (ID) to fungi, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_Sequence conservation in Metazoans (% ID)', 
       'Description'] = 'Protein sequence % identity (ID) to metazoans, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_Sequence conservation in plants (% ID)', 
       'Description'] = 'Protein sequence % identity (ID) to plants, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'

df.loc[df['Feature name'] == 'con_dNdS - A. lyrata', 
       'Description'] = 'Nonsynonymous (dN)/synonymous (dS) substitution rates (also called ka/ks)  between A. thaliana paralogs, and homologs from A. lyrata, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_dNdS - P. trichocarpa', 
       'Description'] = 'Nonsynonymous (dN)/synonymous (dS) substitution rates (also called ka/ks)  between A. thaliana paralogs, and homologs from P. trichocarpa, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_dNdS - V. vinifera', 
       'Description'] = 'Nonsynonymous (dN)/synonymous (dS) substitution rates (also called ka/ks)  between A. thaliana paralogs, and homologs from V. vinifera, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_dNdS with putative paralog', 
       'Description'] = 'Nonsynonymous (dN)/synonymous (dS) substitution rates (also called ka/ks)  between A. thaliana paralogs, and homologs from A. lyrata, P. trichocarpa, V. vinifera, O. sativa and P. patens, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'
df.loc[df['Feature name'] == 'con_dS with putative paralog', 
       'Description'] = 'Synonymous (dS) substitution rates with putative paralog, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'

# DGE features
for dge_cat in ['DGE_general molecular function (dge)', 
                'DGE_growth and development (dge)',
                'DGE_light and circadian (dge)',
                'DGE_stress and stimulus (dge)',
                'DGE_infection and immunity (dge)']:
    dge_expt_names = df.loc[df['Category'] == dge_cat,
                            'Feature name'].str.split('_').str[1]
    names_url = ', obtained from differential gene experiments (DGE) at https://www.ebi.ac.uk/arrayexpress/experiments/' + dge_expt_names.astype(str)
    new_names = df.loc[df['Category'] == dge_cat, 
                       'Description'].str.cat(names_url)
    
    df.loc[df['Category'] == dge_cat, 
           'Description'] = new_names

# Diurnal features
df.loc[df['Feature name'] == 'dia_AMP', 
       'Description'] = 'Amplitude of diurnal gene expression, obtained from https://diurnal.sbs.ntu.edu.sg/'

hour = df.loc[df['Category'] == 'Gene expression, diurnal timepoint (dit)', 
              'Feature name'].str.split('_').str[1]
time_obj = pd.to_datetime(hour.str.replace('.', '', regex=False), format='%H%M').dt.time
time_formatted = time_obj.astype(str).str[:5]
time_clock = 'Timepoint (' + time_formatted + ', 24h clock)'
partial = df.loc[df['Category'] == 'Gene expression, diurnal timepoint (dit)', 
                 'Description'].str.replace('Timepoint', '')
final_desc = time_clock.str.cat(partial)
final_desc = final_desc.astype(str) + ', obtained from https://diurnal.sbs.ntu.edu.sg/'
df.loc[df['Category'] == 'Gene expression, diurnal timepoint (dit)', 
       'Description'] = final_desc

# Epigenetics
df.loc[df['Feature name'] == 'gbm_Gene body methylated', 
       'Description'] = 'Whether gene body is methylated, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'

# GO features
# GO desc
GO_temp = df.loc[df['Category'] == 'GO_BP terms, experimental annotation (go)', 'Description']
GO_temp = GO_temp.str.replace('GO_BP', 'GO_biological_process')
GO_new = GO_temp.astype(str) + ', obtained from the Gene Ontology (GO) database http://geneontology.org/'
df.loc[df['Category'] == 'GO_BP terms, experimental annotation (go)', 
       'Description'] = GO_new 

GO_temp = df.loc[df['Category'] == 'GO_MF terms, experimental annotation (go)', 'Description']
GO_temp = GO_temp.str.replace('GO_MF', 'GO_molecular_function')
GO_new = GO_temp.astype(str) + ', obtained from the Gene Ontology (GO) database http://geneontology.org/'
df.loc[df['Category'] == 'GO_MF terms, experimental annotation (go)', 
       'Description'] = GO_new

GO_temp = df.loc[df['Category'] == 'GO_CC terms, experimental annotation (go)', 'Description']
GO_temp = GO_temp.str.replace('GO_CC', 'GO_cellular_component')
GO_new = GO_temp.astype(str) + ', obtained from the Gene Ontology (GO) database http://geneontology.org/'
df.loc[df['Category'] == 'GO_CC terms, experimental annotation (go)', 
       'Description'] = GO_new  

# GO domain
GO_temp = df.loc[df['Category'] == 'GO_BP terms, experimental annotation (go)', 'Category']
df.loc[df['Category'] == 'GO_BP terms, experimental annotation (go)', 
       'Category'] = GO_temp.str.replace('GO_BP', 'GO_biological_process') 

GO_temp = df.loc[df['Category'] == 'GO_MF terms, experimental annotation (go)', 'Category']
df.loc[df['Category'] == 'GO_MF terms, experimental annotation (go)', 
       'Category'] = GO_temp.str.replace('GO_MF', 'GO_molecular_function')

GO_temp = df.loc[df['Category'] == 'GO_CC terms, experimental annotation (go)', 'Category']
df.loc[df['Category'] == 'GO_CC terms, experimental annotation (go)', 
       'Category'] = GO_temp.str.replace('GO_CC', 'GO_cellular_component')  

# GWAS features
trait = df.loc[(df['Category'] == 'Genome wide association (gwa)'), 
               'Feature name'].str.split('_').str[1]
df.loc[(df['Category'] == 'Genome wide association (gwa)'), 
       'Description'] = 'Genomic loci within genes, correlated with phenotype traits, ' + trait.astype(str) + ', obtained from AtMAD at http://119.3.41.228/atmad/index.php'
new = df.loc[df['Feature name'] == 'gwa_DSDS50', 
             'Description'].str.replace('DSDS50', 
                                        'days of seed dry storage required to reach 50% germination (DSDS50)')
df.loc[df['Feature name'] == 'gwa_DSDS50', 'Description'] = new


# Homolog features
split_species = df.loc[df['Category'] == 'Homologs in other species (hom)', 
                       'Feature name'].str.split('_').str[1:]
species = split_species.str.join(' ')
removed_extra = df.loc[df['Category'] == 'Homologs in other species (hom)', 
                       'Description'].str.replace('23 species (plants and algae)', 
                                                  '', regex=False)
temp = removed_extra.str.cat(species)
new = temp.astype(str) + ', obtained from https://evorepro.sbs.ntu.edu.sg/'
df.loc[df['Category'] == 'Homologs in other species (hom)', 
                       'Description'] = new

# Protein domain features
df.loc[df['Feature name'] == 'mob_counts', 
       'Description'] = 'Prediction of disordered domains regions, obtained from InterProScan https://www.ebi.ac.uk/interpro/'
df.loc[df['Feature name'] == 'num_counts', 
       'Description'] = 'Number of protein domains, including repeated domains, obtained from InterProScan https://www.ebi.ac.uk/interpro/'
df.loc[df['Feature name'] == 'num_u_counts', 
       'Description'] = 'Number of protein domains, excluding repeated domains, obtained from InterProScan https://www.ebi.ac.uk/interpro/'
df.loc[df['Feature name'] == 'tmh_counts', 
       'Description'] = 'Prediction of transmembrane helices, obtained from InterProScan https://www.ebi.ac.uk/interpro/'
pfam_temp = df.loc[df['Category'] == 'Protein domain (pfa)', 'Feature name'].str.split('_', expand=True)
pfam_temp.rename(columns={0: 'prefix', 1: 'pfa'}, inplace=True)
desc = pfam_temp.merge(pfam_df, how='left', left_on='pfa', right_on='Signature Accession')
'''
# No nans in description
desc['Signature Description'].isna().any()
Out[442]: False
'''
temp = desc.loc[:, ['Signature Description']].astype(str) + ', protein families from the Pfam database, obtained from InterProScan https://www.ebi.ac.uk/interpro/'
df.loc[df['Category'] == 'Protein domain (pfa)', 
       'Description'] = temp.values

# Evolution features
df.loc[df['Feature name'] == 'ntd_Nucleotide diversity', 
                       'Description'] = 'Nucleotide diversity calculated among 80 A. thaliana accessions, obtained from https://academic.oup.com/plcell/article/27/8/2133/6096633'

# Gene family features
df.loc[df['Feature name'] == 'ort_all_og_size', 
       'Description'] = 'Gene family size - all species, obtained from https://evorepro.sbs.ntu.edu.sg/'
df.loc[df['Feature name'] == 'ort_ath_og_size', 
       'Description'] = 'Gene family size - only Arabidopsis, obtained from https://evorepro.sbs.ntu.edu.sg/'

# Tandemly duplicated features
df.loc[df['Feature name'] == 'tan_tandem_dup', 
       'Description'] = 'Whether genes are tandemly duplicated in the same gene family, obtained from https://plants.ensembl.org/index.html'

# Phylostrata features
df.loc[df['Feature name'] == 'phy_phylostrata', 
       'Description'] = 'Phylostrata which genes belong to, obtained from https://evorepro.sbs.ntu.edu.sg/'

# Biochemical features
temp = df.loc[df['Category'] == 'Biochemical (pep)', 'Description']
df.loc[df['Category'] == 'Biochemical (pep)', 
       'Description'] = temp.astype(str) + ', obtained from http://isoelectric.org/'


# PPI features
df.loc[df['Category'] == 'Protein protein interaction, PPI network clusters (pid)', 
                       'Description'] = 'Cluster id, genes which belong to the same PPI cluster, obtained from https://thebiogrid.org/'
desc = df.loc[df['Category'] == 'Protein protein interaction, PPI network features (ppi)', 
              'Description']
df.loc[df['Category'] == 'Protein protein interaction, PPI network features (ppi)', 
       'Description'] = desc.astype(str) + ', obtained from https://thebiogrid.org/'


# PTM features
# First pass
df.loc[df['Category'] == 'Protein post-translation modifications (ptm)', 
       'Description'] = 'Count protein PTMs,'
# Second pass
# Replacing values via lookup tables
ptm_aa = df.loc[df['Category'] == 'Protein post-translation modifications (ptm)', 
                'Feature name'].str.split('_').str[1:]
expanded = df.loc[df['Category'] == 'Protein post-translation modifications (ptm)', 
                 'Feature name'].str.split('_', expand=True)
expanded.drop(columns=[0], inplace=True)
# letter is to make it compatible with my lookup aa_df
expanded.rename(columns={1: 'ptm', 2: 'letter'}, inplace=True)
aa_names = expanded.merge(aa_df, how='left', on='letter')
proper_names = aa_names.merge(ptm_df, how='left', left_on='ptm', right_on='short_form')
# Creating final description
temp = df.loc[df['Category'] == 'Protein post-translation modifications (ptm)', 
              'Description'].str.cat(proper_names.loc[:, ['name', 'ptm_y']].values, sep=' ')
new = temp.astype(str) + ', obtained from https://www.psb.ugent.be/webtools/ptm-viewer/index.php'
df.loc[df['Category'] == 'Protein post-translation modifications (ptm)', 
       'Description'] = new

# Genomic information features
df.loc[df['Feature name'] == 'sin_single_copy', 
           'Description'] = 'Whether >1 genes are present in the same gene family, obtained from https://plants.ensembl.org/index.html'


# TPM features
# First pass
for tpm in ['tpm_mad', 'tpm_max', 'tpm_mean', 'tpm_median', 'tpm_min', 
            'tpm_var']:
    exact_name = tpm.split('_')[1]    
    tpm_desc = df.loc[df['Feature name'] == tpm, 'Description']
    new_desc = tpm_desc.astype(str) + ', ' + exact_name + ', obtained from https://evorepro.sbs.ntu.edu.sg/'
    df.loc[df['Feature name'] == tpm, 'Description'] = new_desc

# Second pass for those which need it
df.loc[df['Feature name'] == 'tpm_mad', 'Description'] = 'Level of gene expression - summary statistics, median absolute deviation (MAD), obtained from https://evorepro.sbs.ntu.edu.sg/'
df.loc[df['Feature name'] == 'tpm_var', 'Description'] = 'Level of gene expression - summary statistics, variance, obtained from https://evorepro.sbs.ntu.edu.sg/'

# SPM features
spm = df.loc[(df['Category'] == 'Gene expression (spm)'), 
             'Feature name'].str.split('_').str[1].str.lower()
df.loc[(df['Category'] == 'Gene expression (spm)'), 
       'Description'] = 'Specificity of gene expression in tissues, ' + spm.astype(str) + ', obtained from https://evorepro.sbs.ntu.edu.sg/'

# TF-TG features
temp = df.loc[df['Category'] == 'Transcription factor-target gene features (ttf)',
              'Feature name'].str.split('_').str[1]
new = temp.astype(str) + ', biological characteristics of target genes (TG) of transcription factors, obtained from https://academic.oup.com/nar/article/48/20/11347/5940494'
df.loc[df['Category'] == 'Transcription factor-target gene features (ttf)', 
       'Description'] = new

df.loc[df['Category'] == 'Gene regulatory network clusters (tti)', 
       'Description'] = 'Cluster id, genes which belong to the same gene regulatory cluster, obtained from https://academic.oup.com/nar/article/48/20/11347/5940494'

desc = df.loc[df['Category'] == 'Gene regulatory network features (ttr)', 
              'Description']
df.loc[df['Category'] == 'Gene regulatory network features (ttr)', 
       'Description'] = desc.astype(str) + ', obtained from  https://academic.oup.com/nar/article/48/20/11347/5940494'

# TWAS features
trait = df.loc[df['Category'] == 'Transcriptome wide association (twa)', 
               'Feature name'].str.split('_').str[1]
df.loc[(df['Category'] == 'Transcriptome wide association (twa)'), 
       'Description'] = 'Gene expression level, correlated with phenotype traits, ' + trait.astype(str) + ', obtained from AtMAD at http://119.3.41.228/atmad/index.php'

new_df = df
new_df.index.name = 'id'
new_df.to_csv(OUTPUT, sep='\t')
