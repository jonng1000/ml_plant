# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:08:17 2020

@author: weixiong001

Run RF model with pipeline and other objects to perform the entire machine learning
workflow without data leakage. This workflow uses 5-fold cv. ColumnTransformer,
RandomForestClassifier and cross_val_score have the n_jobs parameter.
"""
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
from datetime import datetime

# Input variables
data_file = sys.argv[1]  # ml data file


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
# 5-fold cv
scores = cross_val_score(clf, X, y, cv=5, scoring='f1', n_jobs=-1)
print('all scores:', scores)
print('f1 mean:', scores.mean())
print('f1 std:', scores.std())

print('Script end:', get_time())
