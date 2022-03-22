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
from sklearn.model_selection import learning_curve
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_curve, auc
from sklearn.model_selection import GridSearchCV

df = pd.read_csv("processed_data_ML.csv", sep="\t", index_col=0)
df_targets = df['Category']
df_features = df.drop(['Category'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(df_features, df_targets,
                                                    test_size=.2)

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

svm = SVC(class_weight='balanced')

grid_param = {
        'kernel': ['linear', 'rbf'],
        'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        'gamma': [0.001, 0.01, 0.1, 1, 10, 100]
}
# Note: When C has 5 parameters and gamma has 4 parameters, takes <1min
# When C has 7 and gamma has 6 parameters, takes ~2min

gd_sr = GridSearchCV(estimator=svm, param_grid=grid_param,
                     scoring='precision', cv=10, n_jobs=-1)
gd_sr.fit(X_train_scaled, y_train)

best_parameters = gd_sr.best_params_
print(best_parameters)
best_result = gd_sr.best_score_
print(best_result)
# Results below
#print(best_parameters)
#{'C': 0.1, 'gamma': 100, 'kernel': 'rbf'}
#print(best_result)
#0.2248580697485807

svm = SVC(C=0.1, gamma=100, kernel='rbf', class_weight='balanced')
train_size = np.linspace(.1, 1, 10)
sample_sizes, train_score, valid_score = learning_curve(svm, 
               X_train_scaled, y_train, train_sizes=train_size,
               verbose=1, cv=10)

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

svm.fit(X_train_scaled, y_train)
y_hat = svm.predict(X_test_scaled)
print(classification_report(y_test, y_hat))
#              precision    recall  f1-score   support
#
#           0       0.92      0.99      0.95       282
#           1       0.33      0.07      0.12        27
#
#    accuracy                           0.91       309
#   macro avg       0.63      0.53      0.54       309
#weighted avg       0.87      0.91      0.88       309
#
# precision: TP/(TP+FP) -> out of all your selected SM genes,
# how many are actually SM genes?
# recall: TP/(TP+FN) -> out of all the total number of actual SM genes,
# how many SM genes did I select?

prob_sgd = svm.decision_function(X_test_scaled)
fpr, tpr, _ = roc_curve(y_test, prob_sgd)
auc_sgd = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(8,8))
ax.plot(fpr, tpr)
ax.plot([0.0, 1.0], [0.0, 1.0], 'r-')
ax.set_xlabel('1-specificity/FPR')
ax.set_ylabel('sensitivity/TPR')
plt.grid()
plt.title('AUC: %.2f' %auc_sgd)
plt.figure()