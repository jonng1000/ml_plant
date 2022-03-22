# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:54:09 2019

@author: weixiong001

Ensemble model
"""

import pandas as pd
import math
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

df = pd.read_csv("combined_results.csv", sep="\t", index_col=0)
y_test = pd.read_csv("raw_output/y_test.csv", sep="\t", index_col=0, header=None)
only_yhat = df[df['result_type'] == 'y_hat']
avg_pred = only_yhat.groupby(['ml']).mean()


# Using majority vote
#len(avg_pred) represents number of ML methods used
threshold = math.ceil(len(avg_pred)/2)
total_votes = avg_pred.sum()
ensemble_predict = (total_votes >= threshold).astype(int)
tn, fp, fn, tp = confusion_matrix(y_test, ensemble_predict).ravel()
tpr = tp / (tp + fn)
tnr = tn / (tn + fp)
SM = classification_report(y_test, ensemble_predict, output_dict=True)['1']

saved = pd.Series([tn, fp, fn, tp, tpr, tnr, SM['precision'], SM['recall'],
                   SM['f1-score']], 
                  index=['tn', 'fp', 'fn', 'tp', 'tpr','tnr', 'precision',
                          'recall', 'f1-score']
                  )
saved.to_csv('em_results_single.csv', sep='\t')

# Using majority vote, converts labels to whole numbers
# marek says this meta score doesn't have to be done now, can be done later
# Decided to try it anyway, just to see
# Uses threshold from above

final_avg_pred = (avg_pred >= 0.5).astype(int)
diff_total_votes = final_avg_pred.sum()
diff_ensemble_predict = (diff_total_votes >= threshold).astype(int)
d_tn, d_fp, d_fn, d_tp = confusion_matrix(y_test, diff_ensemble_predict).ravel()
d_tpr = d_tp / (d_tp + d_fn)
d_tnr = tn / (d_tn + d_fp)


def get_tpn(test, predict):
    tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    return [tn, fp, fn, tp, tpr, tnr]


# Lowered threshold
l_threshold = 2
# Relies on code from above (first majority vote section)
l_ensemble_predict = (total_votes >= l_threshold).astype(int)
l_results = get_tpn(y_test, l_ensemble_predict)

# Lowered threshold
ll_threshold = 1
# Relies on code from above (first majority vote section)
ll_ensemble_predict = (total_votes >= ll_threshold).astype(int)
ll_results = get_tpn(y_test, ll_ensemble_predict)

# Lowered threshold
z_threshold = 0
# Relies on code from above (first majority vote section)
z_ensemble_predict = (total_votes >= z_threshold).astype(int)
z_results = get_tpn(y_test, z_ensemble_predict)

# higher threshold
h_threshold = 4
# Relies on code from above (first majority vote section)
h_ensemble_predict = (total_votes >= h_threshold).astype(int)
h_results = get_tpn(y_test, h_ensemble_predict)

# max threshold
hh_threshold = 5
# Relies on code from above (first majority vote section)
hh_ensemble_predict = (total_votes >= hh_threshold).astype(int)
hh_results = get_tpn(y_test, hh_ensemble_predict)

df_scores = pd.read_csv("combined_scores.csv", sep="\t", index_col=0)
mean_scores = df_scores.groupby(['ml']).mean()
mean_all_ml = mean_scores.mean()

#mean_scores[['tpr', 'tnr']]
#Out[213]: 
#          tpr       tnr
#ml                     
#dtc  0.683095  0.811462
#knn  0.767143  0.825462
#mlp  0.686190  0.787615
#rf   0.742143  0.837462
#svm  0.675714  0.816154

#print(classification_report(y_test, z_ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.00      0.00      0.00       130
#           1       0.24      1.00      0.39        42
#
#    accuracy                           0.24       172
#   macro avg       0.12      0.50      0.20       172
#weighted avg       0.06      0.24      0.10       172
#
#
#print(classification_report(y_test, l_ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.91      0.83      0.87       130
#           1       0.58      0.74      0.65        42
#
#    accuracy                           0.81       172
#   macro avg       0.75      0.78      0.76       172
#weighted avg       0.83      0.81      0.82       172
#
#
#print(classification_report(y_test, ll_ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.91      0.67      0.77       130
#           1       0.43      0.79      0.56        42
#
#    accuracy                           0.70       172
#   macro avg       0.67      0.73      0.66       172
#weighted avg       0.79      0.70      0.72       172
#
#
#print(classification_report(y_test, ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.90      0.92      0.91       130
#           1       0.74      0.67      0.70        42
#
#    accuracy                           0.86       172
#   macro avg       0.82      0.79      0.80       172
#weighted avg       0.86      0.86      0.86       172

#print(classification_report(y_test, h_ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.90      0.94      0.92       130
#           1       0.78      0.67      0.72        42
#
#    accuracy                           0.87       172
#   macro avg       0.84      0.80      0.82       172
#weighted avg       0.87      0.87      0.87       172

#print(classification_report(y_test, hh_ensemble_predict))
#              precision    recall  f1-score   support
#
#           0       0.81      0.98      0.89       130
#           1       0.86      0.29      0.43        42
#
#    accuracy                           0.81       172
#   macro avg       0.83      0.64      0.66       172
#weighted avg       0.82      0.81      0.78       172


##############################################################################


##############################################################################
#Used with: final_avg_pred = (avg_pred >= 0.5).astype(int)
# Need the above as output from individual models need to be converted to only
# 0s and 1s
# Individual models
#print(classification_report(y_test, final_avg_pred.loc['dtc']))
#              precision    recall  f1-score   support
#
#           0       0.90      0.95      0.93       130
#           1       0.82      0.67      0.74        42
#
#    accuracy                           0.88       172
#   macro avg       0.86      0.81      0.83       172
#weighted avg       0.88      0.88      0.88       172
#
#
#print(classification_report(y_test, final_avg_pred.loc['knn']))
#              precision    recall  f1-score   support
#
#           0       0.92      0.83      0.87       130
#           1       0.60      0.79      0.68        42
#
#    accuracy                           0.82       172
#   macro avg       0.76      0.81      0.78       172
#weighted avg       0.84      0.82      0.83       172
#
#
#print(classification_report(y_test, final_avg_pred.loc['svm']))
#              precision    recall  f1-score   support
#
#           0       0.88      0.82      0.85       130
#           1       0.54      0.67      0.60        42
#
#    accuracy                           0.78       172
#   macro avg       0.71      0.74      0.72       172
#weighted avg       0.80      0.78      0.79       172
#
#
#print(classification_report(y_test, final_avg_pred.loc['rf']))
#              precision    recall  f1-score   support
#
#           0       0.91      0.84      0.87       130
#           1       0.60      0.74      0.66        42
#
#    accuracy                           0.81       172
#   macro avg       0.75      0.79      0.77       172
#weighted avg       0.83      0.81      0.82       172
#
#
#print(classification_report(y_test, final_avg_pred.loc['mlp']))
#              precision    recall  f1-score   support
#
#           0       0.88      0.81      0.84       130
#           1       0.53      0.67      0.59        42
#
#    accuracy                           0.77       172
#   macro avg       0.71      0.74      0.72       172
#weighted avg       0.80      0.77      0.78       172
##############################################################################


sum_pred_ml = only_yhat.groupby(['ml']).sum()
sum_pred = sum_pred_ml.sum()
sum_t = len(only_yhat)/2
sum_ensemble_predict = (sum_pred >= sum_t).astype(int)
s_results = get_tpn(y_test, sum_ensemble_predict)

sum_lt = 200
sum_l_predict = (sum_pred >= sum_lt).astype(int)
sl_results = get_tpn(y_test, sum_l_predict)

sum_bt = 300
sum_b_predict = (sum_pred >= sum_bt).astype(int)
sb_results = get_tpn(y_test, sum_b_predict)
