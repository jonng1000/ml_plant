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
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, roc_curve, auc

df = pd.read_csv("processed_data_ML.csv", sep="\t", index_col=0)
df_targets = df['Category']
df_features = df.drop(['Category'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(df_features, df_targets,
                                                    test_size=.2)

# To see how bad is the imbalancing
#y_test.value_counts()
#Out[9]: 
#0    280
#1     29
#Name: Category, dtype: int64
#
#y_train.value_counts()
#Out[10]: 
#0    1156
#1      77
#Name: Category, dtype: int64

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

# Just for exploring, don't actually need to do this
# Hopefully should see that the majoriy of components contribute to the
# variation, and the tail end doesn't contribute much
#from sklearn.decomposition import PCA
#pca = PCA()
#pca.fit(X_train_scaled)
#plt.plot(range(len(pca.explained_variance_ratio_)),
#         pca.explained_variance_ratio_, label='Scree Plot')
#plt.legend()
#plt.figure()
#vr = pca.explained_variance_ratio_
#cvr = [sum(vr[: i + 1]) for i in range(len(vr))]
#plt.plot(range(1, len(cvr) + 1), cvr, 'go-')
#plt.figure()

sgd = SGDClassifier(loss='log', eta0=.01)
train_size = np.linspace(.1, 1, 10)
sample_sizes, train_score, valid_score = learning_curve(sgd, 
               X_train_scaled, y_train, train_sizes=train_size,
               verbose=1, cv=10)
# Verbose output
#[learning_curve] Training set sizes: [ 110  221  332  443  554  665  776  887  998 1109]
#[Parallel(n_jobs=1)]: Using backend SequentialBackend with 1 concurrent workers.
#[Parallel(n_jobs=1)]: Done 100 out of 100 | elapsed:    0.5s finished

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

sgd.fit(X_train_scaled, y_train)
#SGDClassifier(alpha=0.0001, average=False, class_weight=None,
#              early_stopping=False, epsilon=0.1, eta0=0.0, fit_intercept=True,
#              l1_ratio=0.15, learning_rate='optimal', loss='log', max_iter=1000,
#              n_iter_no_change=5, n_jobs=None, penalty='l2', power_t=0.5,
#              random_state=None, shuffle=True, tol=0.001,
#              validation_fraction=0.1, verbose=0, warm_start=False)
y_hat = sgd.predict(X_test_scaled)
#print(classification_report(y_test, y_hat))
#              precision    recall  f1-score   support
#
#           0       0.93      1.00      0.96       288
#           1       0.00      0.00      0.00        21
#
#    accuracy                           0.93       309
#   macro avg       0.47      0.50      0.48       309
#weighted avg       0.87      0.93      0.90       309
#
#C:\ProgramData\Anaconda3\lib\site-packages\sklearn\metrics\classification.py:1437:
# UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
#  'precision', 'predicted', average, warn_for)

# precision: TP/(TP+FP) -> out of all your selected SM genes,
# how many are actually SM genes?
# recall: TP/(TP+FN) -> out of all the total number of actual SM genes,
# how many SM genes did I select?


prob_sgd = sgd.decision_function(X_test_scaled)
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