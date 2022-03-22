# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:14:17 2020

@author: weixiong001

Improved version of build_RF_score. Builds features block by block, with a RF model.
Includes both original and randomly shuffled features.
"""

import pandas as pd 
import rfe_module_v2 as rfm

print('Started script',rfm.get_time())

# Things I need to modify
# Input files and variables
num = 9537  # top x most important features
runs = 100 # number of runs for ml model
s = 9537  # starting number for iterating through features
e = 9537 + 1  # ending number for iterating through features
block = 1  # how many features to put in model during each iteration
# Feature importance, without random features
feat_file = "../feat_impt_orig.txt"
# Dataset of features for ML training
ml_data = "D:/GoogleDrive/machine_learning/RF_PNAS/fully_processed.txt"
class_labels = 'AraCyc annotation'

# Output files and variables
# File to save scores
scores_file = 'rfm_scores_9537.txt'

# Working code, try not to modify it
# Get top 100 features
data = pd.read_csv(feat_file, sep="\t", index_col=0)
data['mean'] = data.mean(axis=1)
top = data.sort_values(by='mean', ascending=False).iloc[:num, :]
top.reset_index(inplace=True)
top_feat = top['features']

df = rfm.read_df(ml_data)  # Will be replaced by another df value below

# Iterate through them 10 by 10

runs_s = []
for i in range(s, e, block):
    model_scores = []
    
    print('Started iteration', i/block,rfm.get_time())
    features = top_feat.iloc[:i]
    features_labels = features.append(pd.Series(['AraCyc annotation']),
                                      ignore_index=True)
    new_df = df[features_labels]  # Replaces orig df variable
    SM_data, GM_data = rfm.sep_df(new_df, class_labels)
    # Each iteration, create and score RF model 100 times
    for j in range(runs):
        SM_test, GM_test, train_df = rfm.split_test_train(SM_data, GM_data, 40, new_df)
        y_train, X_train, y_test, X_test = rfm.sep_feat_labels(train_df,
                                                               class_labels,
                                                               SM_test, GM_test)
        
        # Balance via undersampling majority class
        balance_train = rfm.balancing(X_train, y_train, class_labels)
        # X_train and y_train variables from train_test_split are now
        # reassigned to this
        X_train = balance_train.drop([class_labels], axis=1)
        y_train = balance_train[class_labels]
        
        # Without random shuffling of features
        scaling_obj, X_train_scaled = rfm.scales_continous(X_train)
        X_test_scaled = rfm.scales_test(scaling_obj, X_test)
        rf_model, y_hat = rfm.random_forest(X_train_scaled, y_train, X_test_scaled)
        one_run = rfm.scores(y_test, y_hat)
        ran = pd.Series(['n'], index=['random']) # no random shuffling
        one_run = ran.append(one_run)
        model_scores.append(one_run)
        
        # With random shuffling of features
        X_train = X_train.apply(lambda x: x.sample(frac=1).values)
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
