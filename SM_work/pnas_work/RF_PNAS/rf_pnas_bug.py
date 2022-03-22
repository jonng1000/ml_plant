# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Tried to improve on the rf_pnas.py script, but there's a bug, so dont use this
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score
from datetime import datetime

file = 'fully_processed.txt'
runs = 5
class_labels = 'AraCyc annotation'
scores_file = 'rf_scores.txt'

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print("Script started:", get_time())
print()

df = pd.read_csv(file, sep='\t', index_col=0)

# df.dtypes.astype(str).value_counts()
# Out[3]: 
# int64      9478
# float64      60
# dtype: int64

# df.isna().sum().sum()
# Out[4]: 0

# Based on LabelEncoder from fully_proc.py
SM_data = df[df[class_labels] == 1]
GM_data = df[df[class_labels] == 0]

model_scores = []

def split_test_train(pos_class, neg_class, sample_size, a_df):
    '''
    
    Parameters
    ----------
    pos_class : dataframe
        dataframe containing only the positive class
    neg_class : dataframe
        dataframe containing only the positive class
    sample_size : int
        size of the test set ()
    a_df : dataframe
        entire dataset

    Returns
    -------
    pos_test : dataframe
        positive class, test set
    neg_test : dataframe
        negative class, test set
    train_df : dataframe
        training set

    '''
    pos_test = pos_class.sample(sample_size)
    neg_test = neg_class.sample(sample_size)
    train = a_df.drop(pos_test.index)
    train = a_df.drop(neg_test.index)
    return pos_test, neg_test, train

def sep_feat_labels(train, class_labels, pos_test, neg_test):
    '''

    Parameters
    ----------
    train : dataframe
        training dataset
    class_labels : string
        names of classes
    pos_test : dataframe
        positive class, test set
    neg_test : dataframe
        negative class, test set

    Returns
    -------
    train_labels : series
        class labels, training set
    train_features : dataframe
        training dataset
    test_labels : series
        class labels, test set
    test_features : dataframe
        testing dataset

    '''
    train_labels = train[class_labels]
    train_features = train.drop([class_labels], axis=1)
    test_concat = pd.concat([pos_test, neg_test])
    test_labels = test_concat[class_labels]
    test_features = test_concat.drop([class_labels], axis=1)
    return train_labels, train_features, test_labels, test_features

def balancing(train_features, train_labels):
    '''
    

    Parameters
    ----------
    train_features : dataframe
        features in training set
    train_labels : series
        labels in training set

    Returns
    -------
    df_train_balanced : dataframe
        balanced training set

    '''
    df_train_combined = pd.concat([train_features, train_labels], axis=1)
    df_0 = df_train_combined[df_train_combined[class_labels] == 0]
    df_1 = df_train_combined[df_train_combined[class_labels] == 1]
    sample_0 = df_0.sample(n=df_train_combined[class_labels].value_counts().loc[1])
    df_train_balanced = pd.concat([sample_0, df_1], axis=0)
    df_train_balanced = shuffle(df_train_balanced)
    return df_train_balanced

def scales_continous(train_features):
    '''

    Parameters
    ----------
    train_features : dataframe
        features in training set

    Returns
    -------
    sc : sklearn object
        standard scaler object
    train_scaled : dataframe
        scaled training dataset

    '''
    sc = StandardScaler()
    float_features = train_features.select_dtypes(include='float64')
    int_features = train_features.select_dtypes(include='int64')
    sc.fit(float_features)
    train_scaled = sc.transform(float_features)
    ts_df = pd.DataFrame(data=train_scaled, index=float_features.index,
                         columns=float_features.columns)
    train_scaled = pd.concat([ts_df, int_features], axis=1, sort=False)
    return sc, train_scaled

def scales_test(sc_obj, test_features):
    '''
    

    Parameters
    ----------
    sc_obj : sklearn object
        standard scaler object
    test_features : dataframe
        features in test set

    Returns
    -------
    test_scaled : dataframe
        scaled test set

    '''
    float_features = test_features.select_dtypes(include='float64')
    int_features = test_features.select_dtypes(include='int64')
    test_scaled = sc_obj.transform(float_features)
    ts_df = pd.DataFrame(data=test_scaled, index=float_features.index,
                           columns=float_features.columns)
    test_scaled = pd.concat([ts_df, int_features], axis=1, sort=False)
    return test_scaled

def random_forest(train_scaled, labels, test_scaled):
    '''

    Parameters
    ----------
    train_scaled : dataframe
        scaled training dataset
    labels : series
        ground truth class labels
    test_scaled : dataframe
        scaled testing dataset

    Returns
    -------
    predictions : int array
        class predictions

    '''
    rf = RandomForestClassifier()
    rf.fit(train_scaled, labels)
    predictions = rf.predict(test_scaled)
    return predictions    

def scores(true_labels, predictions):
    '''

    Parameters
    ----------
    true_labels : series
        class labels in test set
    predictions : int array
        class predictions

    Returns
    -------
    run : series
        scores for one run

    '''
    tn, fp, fn, tp = confusion_matrix(true_labels, predictions).ravel()
    f1 = f1_score(true_labels, predictions)
    pre = precision_score(true_labels, predictions)
    re = recall_score(true_labels, predictions) 
    run = pd.Series([tn, fp, fn, tp, f1, pre, re],
                    index=['tn', 'fp', 'fn', 'tp', 'f1', 'precision',
                           'recall'], name='run')
    return run
    

for i in range(runs):
    print('Started iteration', i+1, get_time())
    SM_test, GM_test, train_df = split_test_train(SM_data, GM_data, 40, df)
    y_train, X_train, y_test, X_test = sep_feat_labels(train_df,
                                                       class_labels,
                                                       SM_test, GM_test)
    # Balance via undersampling majority class
    balance_train = balancing(X_train, y_train)
    # X_train and y_train variables from train_test_split are now
    # reassigned to this
    X_train = balance_train.drop([class_labels], axis=1)
    y_train = balance_train[class_labels]
    
    scaling_obj, X_train_scaled = scales_continous(X_train)
    X_test_scaled = scales_test(scaling_obj, X_test)
    
    y_hat = random_forest(X_train_scaled, y_train, X_test_scaled)
    one_run = scores(y_test, y_hat)
    model_scores.append(one_run)
    
df_scores = pd.concat(model_scores, axis=1).T
df_scores.reset_index(drop=True, inplace=True)
df_scores.index.name = 'runs'
df_scores.to_csv(scores_file, sep='\t')
print('Script finished', get_time())
