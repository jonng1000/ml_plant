# -*- coding: utf-8 -*-
"""
Created on 260821

@author: weixiong
Creates DGE labels used for ml, together with the DGE category

Has 448 DGEs, 12 more than expected. ML used 436. Not sure why but nvm,
just ignore. See add_DGE_grps.py in
D:\GoogleDrive\machine_learning\ml_scores_overall for more info
"""

import pandas as pd

FILE = 'DGE_labels_categories.tsv'
OUTPUT = 'DGE_category.txt'

df = pd.read_csv(FILE, sep='\t', index_col=0)
df.drop(columns=['Annotation1', 'Annotation2', 'Notes'], inplace=True)
# Helps to remove duplicate runs, as thats an issue with the raw metadata
df.drop_duplicates(inplace=True)
df.reset_index(inplace=True)


all_ind_dge = []
grouped = df.groupby('Experiment')
for name, group in grouped:
    # Takes care of the situation where there's only one type of test and control
    # samples
    if set(group['Control_test_label']) == {'control_1', 'test_1'}:
        group.drop(columns=['Run'], inplace=True)
        group.drop_duplicates(inplace=True)
        group['Experiment'] = ['dge_' + name + '_up', 'dge_' + name + '_down']
        group.drop(columns=['Control_test_label'], inplace=True)
        all_ind_dge.append(group)
        # Finishes processing experiments when this set of criteria is met, so
        # wanna skip the below if blocks and go to the next iteration, to
        # avoid errors
        continue
    
    # Takes care of the situation where there's more than one type of test
    # and control
    # samples, but each control is only paired with one type of test sample     
    temp_set = {cond_type[-1] for cond_type in \
                group['Control_test_label'].unique()}
    if 'a' not in temp_set:
        for cond_type in group['Control_test_label'].unique():
            if cond_type.startswith('control'):
                group.drop(columns=['Run'], inplace=True)
                group.drop_duplicates(inplace=True)
                group['p1'] = 'dge'
                p2 = group['Control_test_label'].str.split('_').str[1]
                group['p2'] = p2
                group.drop(columns=['Control_test_label'], inplace=True)
                group.drop_duplicates(inplace=True)
                temp_group = group.copy()
                # Putting up and down preffixes to each experiment in order,
                # prevents any error due to experimental order, altho there's
                # a low chance of this happening
                group['p3'] = 'up'
                group['Experiment'] = group.loc[:, ['p1', 'Experiment', 'p2', 'p3']].agg('_'.join, axis=1)
                temp_group['p3'] = 'down'
                temp_group['Experiment'] = temp_group.loc[:, ['p1', 'Experiment', 'p2', 'p3']].agg('_'.join, axis=1)
                new_group = pd.concat([group, temp_group])
                new_group.drop(columns=['p1', 'p2', 'p3'], inplace=True)
                all_ind_dge.append(new_group)
                # Finish processing this set of experiments, so need to break
                # out of the inner loop, otherwise processing will continue,
                # resulting in an error
                break
        # Finishes processing experiments when this set of criteria is met, so
        # wanna skip the below if blocks and go to the next iteration, to
        # avoid errors
        continue

    # Takes care of the situation where there's more than one type of test
    # and control
    # samples, and there's multiple type of pairings between them
    if 'a' in  temp_set:
        for cond_type in group['Control_test_label'].unique():
            if cond_type.startswith('control'):
                group.drop(columns=['Run'], inplace=True)
                group.drop_duplicates(inplace=True)
                group = group.loc[~group['Control_test_label'].str.contains('control'), :].copy()
                p2 = group['Control_test_label'].str.split('_').str[1]
                group['p2'] = p2
                group['p1'] = 'dge'
                group.drop(columns=['Control_test_label'], inplace=True)
                # Just in case
                group.drop_duplicates(inplace=True)
                temp_group = group.copy()
                # Putting up and down preffixes to each experiment in order,
                # prevents any error due to experimental order, altho there's
                # a low chance of this happening
                group['p3'] = 'up'
                group['Experiment'] = group.loc[:, ['p1', 'Experiment', 'p2', 'p3']].agg('_'.join, axis=1)
                temp_group['p3'] = 'down'
                temp_group['Experiment'] = temp_group.loc[:, ['p1', 'Experiment', 'p2', 'p3']].agg('_'.join, axis=1)
                new_group = pd.concat([group, temp_group])
                new_group.drop(columns=['p1', 'p2', 'p3'], inplace=True)
                all_ind_dge.append(new_group)
                # Finish processing this set of experiments, so need to break
                # out of the inner loop, otherwise processing will continue,
                # resulting in an error
                break
        # Finishes processing experiments when this set of criteria is met, so
        # can just go to the next iteration          
        continue

combined_df = pd.concat(all_ind_dge)
combined_df = combined_df.reset_index(drop=True)
combined_df.index.name = 'id'
combined_df.to_csv(OUTPUT, sep='\t')

