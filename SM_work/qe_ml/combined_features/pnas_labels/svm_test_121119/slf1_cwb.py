# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:27:54 2019

@author: weixiong001
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from datetime import datetime

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print("Script started:", get_time())
print() 
plt.ioff() # Turn off inline plotting

df = pd.read_csv("proc_PNAS_data_ML.csv", sep="\t", index_col=0)
df_targets = df['Category']
df_features = df.drop(['Category'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(df_features, df_targets,
                                                    test_size=.1, stratify=df_targets)
lst_params = []
for i in range(1):
    print('Started iteration', i+1, get_time())   
    # Scaling my features
    # Need to scale X_test as well, in the ML workshop, I did it later
    X_train_cont = X_train.loc[:, 'mean_exp':'OG_size']
    X_train_cat = X_train.loc[:, 'single_copy':'viridiplantae']
    sc = StandardScaler()
    sc.fit(X_train_cont)
    X_train_cont_scaled = sc.transform(X_train_cont)
    X_tcs_df = pd.DataFrame(data=X_train_cont_scaled, index=X_train_cont.index,
                            columns=X_train_cont.columns)
    X_train_scaled = pd.concat([X_tcs_df, X_train_cat], axis=1, sort=False)
    
    X_test_cont = X_test.loc[:, 'mean_exp':'OG_size']
    X_test_cat = X_test.loc[:, 'single_copy':'viridiplantae']
    X_test_cont_scaled = sc.transform(X_test_cont)
    X_testcs_df = pd.DataFrame(data=X_test_cont_scaled, index=X_test_cont.index,
                            columns=X_test_cont.columns)
    X_test_scaled = pd.concat([X_testcs_df, X_test_cat], axis=1, sort=False)
    print('Finished oversampling and scaling')
    print('Starting grid search', get_time())
    svm = SVC(class_weight='balanced') 
    grid_param = {
            'kernel': ['linear', 'rbf'],
            'C': [0.001, 0.01, 0.1, 1, 10],
            'gamma': [0.001, 0.01, 0.1, 1]
    }
    gd_sr = GridSearchCV(estimator=svm, param_grid=grid_param,
                         scoring='f1', cv=10, n_jobs=-1)
    gd_sr.fit(X_train_scaled, y_train)
    best_parameters = pd.Series(gd_sr.best_params_)
    # Appending gridsearch results to save it
    lst_params.append(best_parameters)
    
df_params = pd.DataFrame(lst_params)
freq_params = df_params.groupby(list(df_params.columns)).size().reset_index()
freq_params.rename(columns={0: "Freq"}, inplace=True)
idx = freq_params['Freq'].idxmax()
best_params = freq_params.iloc[idx]

# Creating model
svm = SVC(C=best_params['C'], gamma=best_params['gamma'],
          kernel=best_params['kernel'])    
print('Fitting model')
svm.fit(X_train_scaled, y_train)
y_hat = svm.predict(X_test_scaled)
# Generating series to save model predictions
ytest_series = pd.Series(y_test, name='y_test').reset_index(drop=True)
yhat_series = pd.Series(y_hat, name='y_hat')
prob_sgd = svm.decision_function(X_test_scaled)
prob_series = pd.Series(prob_sgd, name='prob')
tn, fp, fn, tp = confusion_matrix(y_test, y_hat).ravel()
tpr = tp / (tp + fn)
tnr = tn / (tn + fp)
one_run = pd.Series([tn, fp, fn, tp, tpr, tnr],
                    index=['tn', 'fp', 'fn', 'tp', 'tpr', 'tnr'],
                    name='score')
print()

print('Printing dataframes', get_time())
df_params = pd.DataFrame(lst_params)
df_params.to_csv('params_matrix.csv', sep='\t')
df_results = pd.DataFrame([ytest_series, yhat_series, prob_series])
df_results.to_csv('params_results.csv', sep='\t')
one_run.to_csv('all_scores.csv', sep='\t')
print('Script finished', get_time())
