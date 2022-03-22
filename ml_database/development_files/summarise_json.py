# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 19:28:47 2022

@author: weixiong001

Summaries final processed file into json, and ensures format is compatible
with Swee Kwang's overallData.json format.
Used to create a smaller table for the front page.
"""

import pandas as pd
import json

FILE = 'processed_stage4.txt'
OUTPUT = 'summariseData.json'

df = pd.read_csv(FILE, index_col=0 , sep='\t')
df = df.rename(columns={'Category': 'category', 'Feature name': 'feature',
                        'Description':'description'})
df['id'] = '-'

combined_set = {'agi_cluster_id_1000', 'agn_cluster_size', 'pep_aal', 
                'cif_ABI3VP1', 'cin_ABFs binding site motif', 
                'con_Sequence conservation in plants (% ID)',
                'dge_E-GEOD-10968_1a_down', 'dge_E-GEOD-35288_down', 'dge_E-MTAB-4226_1a_up',
                'dge_E-GEOD-38879_1a_down', 'dge_E-GEOD-54680_1_down', 'gbm_Gene body methylated',
                'ntd_Nucleotide diversity', 'cid_cluster_id_1', 'coe_bet_cen',
                'spm_Apical meristem', 'tpm_mad', 'dia_AMP', 'dit_0.0', 'ort_all_og_size',
                'tti_cluster_id_1', 'ttr_bet_cen', 'gwa_anthocyanin content',
                'sin_single_copy', 'tan_tandem_dup', 'go_GO_0006950', 'go_GO_0009507',
                'go_GO_0005515', 'hom_Amborella_trichopoda', 'phy_phylostrata',
                'mob_counts', 'num_counts', 'pfa_PF00004', 'tmh_counts', 'ptm_ac_K',
                'pid_cluster_id_1', 'ppi_bet_cen',
                'ttf_Difference in length of longest and shortest isoform of protein',
                'twa_arsenic concentration'}

'''
len(combined_set)
Out[537]: 39
'''

summary = df.loc[df['feature'].isin(combined_set), :]
result = summary.to_json(orient="records")
parsed = json.loads(result)
json_object = json.dumps(parsed, indent=4) 

# Writing to sample.json
with open(OUTPUT, 'w') as outfile:
    outfile.write(json_object)

