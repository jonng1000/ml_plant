# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:18 2020

@author: weixiong001

Explore scores from hp tests - see which type of hp gives the best scores
"""

import os
import pandas as pd

'''
# For 71 GO classes
DATA_FOLDER = './all_results/results_71_ohp/'
DATA_FOLDER2 = './all_results/output_71chp/'
DATA_FOLDER3 = './all_results/output_71g1hp/'
DATA_FOLDER4 = './all_results/output_71g2hp/'
DATA_FOLDER5 = './all_results/results_dhp/'
'''
# For 16 GO classes
DATA_FOLDER = './all_results/results_16c_ohp/'
DATA_FOLDER2 = './all_results/output_16chp/'
DATA_FOLDER3 = './all_results/output_16g1hp/'
DATA_FOLDER4 = './all_results/output_16g2hp/'
DATA_FOLDER5 = './all_results/results_16c_dhp/'

def get_scores_lst(folder):
    """
    Get all files in a folder, and from this, select only scores file,
    and returns it as a list of files
    """
    all_files = [a_file for a_file in os.listdir(folder)]
    scores_list = [one for one in all_files if one.endswith('_scores.txt')]
    return scores_list


def produce_df_lst(scores_list, folder):
    """
    From list of scores files, read in all their dataframes to form a list of
    them
    """
    df_lst = []
    for one in scores_list:
        file_path = folder + '/' + one
        go_term = one.split('_')[1] + '_' + one.split('_')[2]
        data = pd.read_csv(file_path, sep='\t', index_col=0)
        data.insert(loc=0, column='class_label', value=go_term)
        df_lst.append(data)
    return df_lst
 
    
def combine(the_folder):
    """
    Combine all the score dataframes from one expt, to form one dataframe
    containing all the scores
    """
    # List of scores files
    sl_orig = get_scores_lst(the_folder)
    # List of scores as df
    lst_df = produce_df_lst(sl_orig, the_folder)
    df_orig = pd.concat(lst_df, axis=0)
    return df_orig


# Creating dataframes
opt_hp = combine(DATA_FOLDER)
opt_hp2 = combine(DATA_FOLDER2)
opt_hp3 = combine(DATA_FOLDER3)
opt_hp4 = combine(DATA_FOLDER4)
d_hp = combine(DATA_FOLDER5)
# Insert column showing if hp optimisation, chosen hps or
# default hps were used
opt_hp.insert(loc=1, column='hp_type', value='rs_optimised')
opt_hp2.insert(loc=1, column='hp_type', value='chosen')
opt_hp3.insert(loc=1, column='hp_type', value='chosen_g1')
opt_hp4.insert(loc=1, column='hp_type', value='chosen_g2')
d_hp.insert(loc=1, column='hp_type', value='default')

combined_df = pd.concat([opt_hp, opt_hp2, opt_hp3, opt_hp4, d_hp], axis=0)
# Sorts by class_label, alphabhetical order, ensures plotting makes sense
combined_df = combined_df.sort_values('class_label')

selected = combined_df.loc[:, ['class_label', 'hp_type', 'oob_f1']]
each_GO_mean = selected.groupby(['class_label', 'hp_type']).mean()
all_mean = selected.groupby(['hp_type']).mean()
'''
# 71 GO classes
selected df
                            oob_f1
class_label hp_type               
GO_0000138  chosen        0.404110
            chosen_g1     0.404110
            chosen_g2     0.404110
            default       0.000000
            rs_optimised  0.401384
                           ...
GO_1990837  chosen        0.177215
            chosen_g1     0.177215
            chosen_g2     0.177215
            default       0.000000
            rs_optimised  0.150538

[355 rows x 1 columns]

all_mean df
                oob_f1
hp_type               
chosen        0.415040
chosen_g1     0.415050
chosen_g2     0.415357
default       0.086755
rs_optimised  0.459666

# 16 GO classes
selected
Out[44]: 
   class_label       hp_type    oob_f1
id                                    
0   GO_0005634  rs_optimised  0.469219
0   GO_0005634     chosen_g1  0.403522
0   GO_0005634     chosen_g2  0.402815
0   GO_0005634        chosen  0.403522
0   GO_0005634       default  0.080849
..         ...           ...       ...
0   GO_0097708     chosen_g2  0.564706
0   GO_0097708        chosen  0.562900
0   GO_0097708  rs_optimised  0.588621
0   GO_0097708     chosen_g1  0.562900
0   GO_0097708       default  0.008282

[80 rows x 3 columns]

all_mean
Out[45]: 
                oob_f1
hp_type               
chosen        0.390290
chosen_g1     0.390379
chosen_g2     0.391213
default       0.090630
rs_optimised  0.426361
'''
