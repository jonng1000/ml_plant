# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:14:17 2020

@author: weixiong001

Edited from build_RF_mi_f200.py at
/mnt/d/GoogleDrive/machine_learning/GO_features/ind_classes/mi/temp_ran.
Builds features block by block, with a RF model.
Uses mutual information (mi) to determine the importance of features.
Includes both original and randomly shuffled features.
Need to change line of code where master list (variable name
is called master, this is the range of values
used to iterate through features) is created, in accordance
with the number of features used.
This script is for randomly selected features, hence its modified
from build_RF_mi_f200.py to account for this
"""

import pandas as pd
import sys
# Can comment out these two lines if running on workstation
# Needed to ensure below module is imported correctly
#PATH = 'D:/GoogleDrive/machine_learning/RF_PNAS/feature_extract'
#sys.path.insert(1, PATH + '/build_top_features')
import rfe_module_v3 as rfm

print('Started script',rfm.get_time())
# Input variables and constants
mi_file = sys.argv[1]  # file with mi of features
ml_data = sys.argv[2]  # dataset
CLASS_LABELS = 'AraCyc annotation'
# Things I need to modify
RUNS = 100 # number of runs for ml model
NUM = 200 # top NUM of features
# Output variables
# File to save scores
scores_file = ml_data.split('_GO.txt')[0] + '_build_s.txt'

##############################################################################
# Working code from here on, try not to modify it

# Get top X features
mutinfo_feat = pd.read_csv(mi_file, sep="\t", index_col=0)
# Dataset with NUM features
df = rfm.read_df(ml_data)
# Sorting dataset's features in order of its mi, from the mi feature file,
# mi_file 
sorted_f_mi = mutinfo_feat.loc[df.columns].sort_values(by='mi', ascending=False)
# Top feature is class label so need to remove it
top_num_f = sorted_f_mi.index[1: NUM+1]

# Codes positive class as 1 and negative class as 0
pos = df[CLASS_LABELS].value_counts().idxmin()
neg = df[CLASS_LABELS].value_counts().idxmax()
print(df[CLASS_LABELS].value_counts())
print('positive class:', pos)
print('negative class:', neg)
df.loc[:, 'AraCyc annotation'].replace([pos, neg], [1, 0], inplace=True)

# Master list to iterate through, to buid RF model
# Need to change this as feature number changes
# Even if there's only one tuple in the list, leave it as a list of tuples
# as if I have multiple tuples, would allow me to iterate over a range of
# features with different step sizes
master = [(10, NUM+1, 10)]

c = 0
runs_s = []

for parameter in master:
    for i in range(parameter[0], parameter[1], parameter[2]):
        model_scores = []
        c+=1
        print('Started iteration', c, rfm.get_time())
        features = top_num_f[:i]
        features_labels = list(features) + ['AraCyc annotation']
        # Used downstream instead of orig df variable
        new_df = df[features_labels]          

        # Checks if there are any float datatypes. There should be
        # If there isn't, flag as warning
        condition = new_df.select_dtypes(include='float64').empty
        if condition:
            print('WARNING: FEATURES', parameter[0], parameter[1], 'HAS NO FLOATS')
        
        SM_data, GM_data = rfm.sep_df(new_df, CLASS_LABELS)
        test_size = int(len(SM_data)/10)
        # Each iteration, create and score RF model 100 times
        for j in range(RUNS):
            SM_test, GM_test, train_df = rfm.split_test_train(SM_data, GM_data,
                                                              test_size, new_df)
            y_train, X_train, y_test, X_test = rfm.sep_feat_labels(train_df,
                                                                   CLASS_LABELS,
                                                                   SM_test, GM_test)
            
            # Balance via undersampling majority class
            balance_train = rfm.balancing(X_train, y_train, CLASS_LABELS)
            # X_train and y_train variables from train_test_split are now
            # reassigned to this
            X_train = balance_train.drop([CLASS_LABELS], axis=1)
            y_train = balance_train[CLASS_LABELS]
            
            # Without random shuffling of features
            # Prevents error when scaling is done on an empty float64 df
            if condition:
                X_train_scaled = X_train
                X_test_scaled = X_test
            else:
                scaling_obj, X_train_scaled = rfm.scales_continous(X_train)
                X_test_scaled = rfm.scales_test(scaling_obj, X_test)
            rf_model, y_hat = rfm.random_forest(X_train_scaled, y_train, X_test_scaled)
            one_run = rfm.scores(y_test, y_hat)
            ran = pd.Series(['n'], index=['random']) # no random shuffling
            one_run = ran.append(one_run)
            model_scores.append(one_run)
            
            # With random shuffling of features
            X_train = X_train.apply(lambda x: x.sample(frac=1).values)
            # Prevents error when scaling is done on an empty float64 df
            if condition:
                X_train_scaled = X_train
                X_test_scaled = X_test
            else:
                scaling_obj, X_train_scaled = rfm.scales_continous(X_train)
                X_test_scaled = rfm.scales_test(scaling_obj, X_test)
            rf_model, y_hat = rfm.random_forest(X_train_scaled, y_train, X_test_scaled)
            one_run = rfm.scores(y_test, y_hat)
            ran = pd.Series(['y'], index=['random'])
            one_run = ran.append(one_run)
            model_scores.append(one_run)
        
        df_scores = pd.concat(model_scores, axis=1).T
        df_scores.reset_index(drop=True, inplace=True)
        df_scores.index.name = 'runs'
        df_scores.insert(0, 'num_features', i)
        runs_s.append(df_scores)
        
all_scores = pd.concat(runs_s)
all_scores.reset_index(inplace=True)
all_scores.index.name = 'id'
all_scores.to_csv(scores_file, sep='\t')        

print('Ended script',rfm.get_time())
