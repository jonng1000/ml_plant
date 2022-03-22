# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Run RF model with pipeline and other objects to perform the entire machine learning
workflow without data leakage. This workflow is ran once just to test, and prints
out the classification report. Only ColumnTransformer and RandomForestClassifier
have the n_jobs parameter.
"""
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score 
from datetime import datetime

# Input variables
data_file = sys.argv[1]  # ml data file
scores_file = data_file.split('_GO')[0] + '_scores.txt'
RUNS = 100

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


print('Script started:', get_time())
# Reads in dataset and replaces positive and negative classes with 1 and 0
# respectively
data = pd.read_csv(data_file, sep='\t', index_col=0)
pos =  data_file.split('_GO')[0].replace('_',' ')
neg = 'not ' + pos
print(data['class_label'].value_counts())
print('positive class:', pos)
print('negative class:', neg)
data.loc[:, 'class_label'].replace([pos, neg], [1, 0], inplace=True)
# Get list of continuous features
ge_features = data.columns[data.columns.str.startswith('GE_')]

# Pipeline object to fill missing NA values with median, and apply standard
# scaling, on continuous features
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])
# preprocessor preprocesses data according to Pipelines above
preprocessor = ColumnTransformer(
    [('num', numeric_transformer, ge_features)],
     remainder='passthrough', n_jobs=-1)

# Pipleline to perform full workflow from preprocessing to model fitting
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',
                       RandomForestClassifier(n_jobs=-1, class_weight='balanced'))
                     ])
X = data.drop(columns=['class_label'])
y = data.loc[:, 'class_label']

model_scores = []
for one_run in range(RUNS):
    print('run', one_run+1, 'started:', get_time())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        stratify=y)
    df_train = pd.concat([X_train, y_train], axis=1)
    df_0 = df_train[df_train['class_label'] == 0]
    df_1 = df_train[df_train['class_label'] == 1]
    # Assumes minority class is the desired and positive class
    sample_0 = df_0.sample(n=df_train['class_label'].value_counts().loc[1])
    df_train_balanced = pd.concat([sample_0, df_1], axis=0)
    df_train_balanced = shuffle(df_train_balanced)
    X_train = df_train_balanced.drop(columns=['class_label'])
    y_train = df_train_balanced.loc[:, 'class_label']
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    f1 = f1_score(y_test, y_pred)
    pre = precision_score(y_test, y_pred)
    re = recall_score(y_test, y_pred) 
    run = pd.Series([tn, fp, fn, tp, f1, pre, re],
                    index=['tn', 'fp', 'fn', 'tp', 'f1', 'precision',
                           'recall'], name='run')
    model_scores.append(run)

df_scores = pd.concat(model_scores, axis=1).T
df_scores.reset_index(drop=True, inplace=True)
df_scores.index.name = 'runs'
df_scores.to_csv(scores_file, sep='\t')
print('Script end:', get_time())
