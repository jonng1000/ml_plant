# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:14:17 2020

@author: weixiong001

Builds features block by block, with a RF model, and randomises it
"""

import pandas as pd 
import rfe_module as rfm

print('Started script',rfm.get_time())

# Input files and variables
num = 100  # top x most important features
runs = 100 # number of runs for ml model
block = 10  # how many features to put in model during each iteration
# Feature importance, without random features
feat_file = "../feat_impt_orig.txt"
# Dataset of features for ML training
ml_data = "D:/GoogleDrive/machine_learning/RF_PNAS/fully_processed.txt"
class_labels = 'AraCyc annotation'

# Output files and variables
# File to save scores
scores_file = 'rfm_scores_ran.txt'
# File to save feature importances
feat_impt_file = 'rfm_feat_ran.txt'

# Get top 100 features
data = pd.read_csv(feat_file, sep="\t", index_col=0)
data['mean'] = data.mean(axis=1)
top = data.sort_values(by='mean', ascending=False).iloc[:num, :]
top.reset_index(inplace=True)
top_feat = top['features']

df = rfm.read_df(ml_data)  # Will be replaced by another df value below

# Iterate through them 10 by 10

runs100 = []
feat100 = []
for i in range(10, 101, block):
    model_scores = []
    feat_impt = []
    
    print('Started iteration', i/10,rfm.get_time())
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
        # Randomly shuffle feature values
        X_train = X_train.apply(lambda x: x.sample(frac=1).values)
        # Balance via undersampling majority class
        balance_train = rfm.balancing(X_train, y_train, class_labels)
        # X_train and y_train variables from train_test_split are now
        # reassigned to this
        X_train = balance_train.drop([class_labels], axis=1)
        y_train = balance_train[class_labels]
        
        scaling_obj, X_train_scaled = rfm.scales_continous(X_train)
        X_test_scaled = rfm.scales_test(scaling_obj, X_test)
        rf_model, y_hat = rfm.random_forest(X_train_scaled, y_train, X_test_scaled)
        one_run = rfm.scores(y_test, y_hat)
        model_scores.append(one_run)
        fi_sort = pd.DataFrame(rf_model.feature_importances_, 
                                index=X_train.columns,
                                columns=['importance']).sort_values('importance',
                                                                    ascending=False)
        feat_impt.append(fi_sort)
    
    df_scores = pd.concat(model_scores, axis=1).T
    df_scores.reset_index(drop=True, inplace=True)
    df_scores.index.name = 'runs'
    df_scores.insert(0, 'num_features', i)
    runs100.append(df_scores)
    
    df_feat_i = pd.concat(feat_impt, axis=1)
    df_feat_i.columns = ['impt' + str(i) for i in range(runs)]
    df_feat_i.index.name = 'features'
    df_feat_i.reset_index(inplace=True)
    df_feat_i.insert(0, 'num_features', i)
    feat100.append(df_feat_i)
    
all_scores = pd.concat(runs100)
all_scores.reset_index(inplace=True)
all_scores.index.name = 'id'
all_scores.insert(0, 'random', 'y')
all_feat = pd.concat(feat100)
all_feat.reset_index(drop=True, inplace=True)
all_feat.index.name = 'id'
all_feat.insert(0, 'random', 'y')

all_scores.to_csv(scores_file, sep='\t')
all_feat.to_csv(feat_impt_file, sep='\t')
# Each iteration, also randomise feature values and do above

# Plot score across iteration, one graph with actual model, one graph with
# randomised feature values

print('Ended script',rfm.get_time())