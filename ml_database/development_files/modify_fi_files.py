# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 1725 2022

@author: weixiong001

Modifies *_fi.txt files to add feature category and description, and FRS.
Output file has the same name as the original *_fi.txt, to make it easy for 
Swee Kwang to update the database.

Takes about 5h
"""

import os
import pandas as pd
from datetime import datetime

GO_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/go_runs/fixed_hps/output4'
DGE_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/dge_runs/output'
CONTF_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/contf_runs/output'
CONTF_MAP = 'G:/My Drive/machine_learning/ml_go_workflow/contf_runs/mod_class_labels_contf.txt'
REST_CATF_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/rest_catf_runs/output'
TTI_FOLDER = 'G:/My Drive/machine_learning/ml_go_workflow/tti_runs/output'
# json file which has feature category and description info
REF_JSON = 'overallData.json'
# FRS table with FRS info
FRS_DATA = 'spearman_values.txt'
OUTPUT_FOLDER = './output_fi'


def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_path(folder):
    """
    Get a list of all *_fi.txt file paths in one folder, which contains
    trained models from a group of features
    """
    temp_files = [folder + '/' + one_file for one_file in os.listdir(folder)]
    all_files = [one_file for one_file in temp_files if one_file.endswith('_fi.txt')]
    return all_files

def modify_fi(one_path, json_data, frs_table):
    """
    From a *_fi.txt file path, modifies *_fi.txt file to include feature category,
    description, and FRS. Also takes in the json file which has feature category
    and description info, and the FRS table with FRS info
    """
    # Preprocessing feature info table
    overall_data = pd.read_json(json_data, orient='records')
    overall_data['feature'] = overall_data['feature'].str.replace('go_GO_','go_GO:')
    overall_data = overall_data.set_index('feature')
    overall_data.index.name = 'features'
    # Preprocessing feature rank score (FRS) table
    frs_df = pd.read_csv(frs_table, index_col=0, delimiter='\t')
    frs_df.index.name = 'features'
    # Loads in mapper for continous features
    contf_map_df = pd.read_csv(CONTF_MAP, index_col=0, header=None, delimiter='\t')
    contf_map_df.rename(columns={1: 'job_ids'}, inplace=True)
    
    if one_path.endswith('_fi.txt'):
        fi_df = pd.read_csv(one_path, index_col=0, delimiter = '\t')
        # Due to prev errors where these features are incorrectly labelled
        fi_df.index = fi_df.index.str.replace('ttr_cluster_id', 'tti_cluster_id')
        temp = fi_df.rename(columns={'rf': 'feature_importance'})
        # Add additional feature info to the feature importance table
        added_infoI = temp.merge(overall_data, how='left', on='features')
        # Check to make sure there is no nan
        if added_infoI.isna().any().any():
            print(one_path, 'nan upon adding feature info')
        added_infoI.drop(columns=['id'], inplace=True)
        
        # Target for getting FRS
        file_name = one_path.split('/')[-1]
        #print(file_name)  # For checking
        # Check if target is GO term
        if file_name.startswith('go_GO'):
            modified = file_name.replace('go_GO_', 'go_GO:')
            target = modified.split('_fi.txt')[0]
        # Check if target is DGE
        elif file_name.startswith('dge_'):
            target = file_name.split('_fi.txt')[0]
        # Check if target is continuous
        elif file_name.startswith('job_'):
            modified = file_name.split('_fi.txt')[0]
            target = contf_map_df.loc[contf_map_df['job_ids'] == modified, :].index[0]
        # Rest of categorical features
        else:
            target = file_name.split('_fi.txt')[0]
        
        # Adds FRS info to table with feature info
        if target in frs_df.columns:
            relevant_values = frs_df.loc[:, [target]]
            relevant_values.rename(columns = {relevant_values.columns[0]: 'FRS'}, inplace = True)
            added_infoII = added_infoI.merge(relevant_values, how='left', on='features')
            added_infoII.fillna('-', inplace=True)
        else:
            added_infoII = added_infoI.copy()
            added_infoII['FRS'] = '-'
            
        finished = (file_name, added_infoII)
    
    return finished

def writes_file(list_info, folder):
    """
    From modified *_fi.txt file, writes it to a folder, output file has same
    name as original *_fi.txt, to make it easy for Swee Kwang to update the
    database
    """
    for one_tuple in list_info:
        file_name = one_tuple[0]
        feat_df = one_tuple[1]
        output_path = folder + '/' + file_name
        feat_df.to_csv(output_path, sep='\t')
    return None


print('GO features start:', get_time())
file_paths = get_path(GO_FOLDER)
#file_paths = file_paths[:2] #  For checking
lst_modified = [modify_fi(item, REF_JSON, FRS_DATA) for item in file_paths]
writes_file(lst_modified, OUTPUT_FOLDER)
print('end:', get_time())

print('DGE features start:', get_time())
file_paths = get_path(DGE_FOLDER)
# For testing
#file_paths = ['G:/My Drive/machine_learning/ml_go_workflow/dge_runs/output/dge_E-MTAB-4226_1a_up_fi.txt']
lst_modified = [modify_fi(item, REF_JSON, FRS_DATA) for item in file_paths]
writes_file(lst_modified, OUTPUT_FOLDER)
print('end:', get_time())

print('continuous features start:', get_time())
file_paths = get_path(CONTF_FOLDER)
#  For testing
#file_paths = file_paths = ['G:/My Drive/machine_learning/ml_go_workflow/contf_runs/output/job_0_fi.txt']
lst_modified = [modify_fi(item, REF_JSON, FRS_DATA) for item in file_paths]
writes_file(lst_modified, OUTPUT_FOLDER)
print('end:', get_time())

print('rest of categorical features start:', get_time())
file_paths = get_path(REST_CATF_FOLDER)
#  For testing
#file_paths = file_paths = ['G:/My Drive/machine_learning/ml_go_workflow/rest_catf_runs/output/agi_cluster_id_1_fi.txt']
lst_modified = [modify_fi(item, REF_JSON, FRS_DATA) for item in file_paths]
writes_file(lst_modified, OUTPUT_FOLDER)
print('end:', get_time())

print('tti features start:', get_time())
file_paths = get_path(TTI_FOLDER)
lst_modified = [modify_fi(item, REF_JSON, FRS_DATA) for item in file_paths]
writes_file(lst_modified, OUTPUT_FOLDER)
print('end:', get_time())

# Loop through all files, get full file path, pass to below
# Modify 1 fi file
# Save output in new folder
