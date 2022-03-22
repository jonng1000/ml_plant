# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Runs RF model with default hyperparameters and plots learning curve
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, roc_curve, auc
from datetime import datetime

file = 'fully_processed.txt'
runs = 1
class_labels = 'AraCyc annotation'

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
df_targets = df[class_labels]
SM_data = df[df[class_labels] == 1]
GM_data = df[df[class_labels] == 0]

for i in range(runs):
    SM_test = SM_data.sample(40)
    GM_test = GM_data.sample(40)
    train_df = df.drop(SM_test.index)
    train_df = train_df.drop(GM_test.index)
    
    y_train = train_df[class_labels]
    X_train = train_df.drop([class_labels], axis=1)
    test_concat = pd.concat([SM_test, GM_test])
    y_test = test_concat[class_labels]
    X_test = test_concat.drop([class_labels], axis=1)
    
    print('Started iteration', i+1, get_time())
    # Balancing
    df_train_combined = pd.concat([X_train, y_train], axis=1)

    df_0 = df_train_combined[df_train_combined[class_labels] == 0]
    df_1 = df_train_combined[df_train_combined[class_labels] == 1]
    
    # undersample
    sample_0 = df_0.sample(n=df_targets.value_counts().loc[1])
    df_train_balanced = pd.concat([sample_0, df_1], axis=0)
    df_train_balanced = shuffle(df_train_balanced)
    
    # X_train and y_train variables from train_test_split are now
    # reassigned to this
    X_train = df_train_balanced.drop([class_labels], axis=1)
    y_train = df_train_balanced[class_labels]
    
    sc = StandardScaler()
    X_train_con = X_train.select_dtypes(include='float64')
    X_train_int = X_train.select_dtypes(include='int64')
    sc.fit(X_train_con)
    X_train_scaled = sc.transform(X_train_con)
    X_tcs_df = pd.DataFrame(data=X_train_scaled, index=X_train_con.index,
                            columns=X_train_con.columns)
    X_train_scaled = pd.concat([X_tcs_df, X_train_int], axis=1, sort=False)
    
    X_test_con = X_test.select_dtypes(include='float64')
    X_test_int = X_test.select_dtypes(include='int64')
    X_test_scaled = sc.transform(X_test_con)
    X_testcs_df = pd.DataFrame(data=X_test_scaled, index=X_test_con.index,
                               columns=X_test_con.columns)
    X_test_scaled = pd.concat([X_testcs_df, X_test_int], axis=1, sort=False)

    print('Finished oversampling and scaling')
    print('Starting RF model', get_time())
    
    rf = RandomForestClassifier()
    rf.fit(X_train_scaled, y_train)
    y_hat = rf.predict(X_test_scaled)
    print(classification_report(y_test, y_hat))

    train_size = np.linspace(.1, 1, 10)
    sample_sizes, train_score, valid_score = learning_curve(rf, 
                   X_train_scaled, y_train, train_sizes=train_size,
                   verbose=1, cv=10, n_jobs=-1)
    
    train_mean = np.mean(train_score, axis=1)
    train_std = np.std(train_score, axis=1)
    valid_mean = np.mean(valid_score, axis=1)
    valid_std = np.std(valid_score, axis=1)
    
    plt.fill_between(sample_sizes, train_mean - train_std, 
                     train_mean + train_std, color='b', alpha=.1)
    plt.plot(sample_sizes, train_mean, 'bo-', label='Training')
    plt.fill_between(sample_sizes, valid_mean - valid_std, 
                     valid_mean + valid_std, color='r', alpha=.1)
    plt.plot(sample_sizes, valid_mean, 'ro-', label='Validation')
    plt.legend()
    plt.figure()
    
