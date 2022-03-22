# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:54:09 2019

@author: weixiong001

Ensemble model by varying alpha (threshold to convert average labels 
[in fractions] into 0s and 1s for individual models)
"""

import pandas as pd
import math
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from matplotlib import pyplot as plt

df = pd.read_csv("combined_results.csv", sep="\t", index_col=0)
y_test = pd.read_csv("raw_output/y_test.csv", sep="\t", index_col=0, header=None)
only_yhat = df[df['result_type'] == 'y_hat']
avg_pred = only_yhat.groupby(['ml']).mean()

def get_tpn(test, predict):
    tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()
    tpr = tp / (tp + fn)
    tnr = tn / (tn + fp)
    return [tn, fp, fn, tp, tpr, tnr]


# alpha specificies the threshold to convert labels to whole numbers
# marek says to try a range of alphas and see the results
alpha = [i/10 for i in range(1,11)]
# Using majority vote, 
#len(avg_pred) represents number of ML methods used
threshold = math.ceil(len(avg_pred)/2)


all_results = []
for i in alpha:
    final_avg_pred = (avg_pred >= i).astype(int)
    total_votes = final_avg_pred.sum()
    ensemble_predict = (total_votes >= threshold).astype(int)
    result = get_tpn(y_test, ensemble_predict)
    SM = classification_report(y_test, ensemble_predict, output_dict=True)['1']
    one_row = [i] + result
    one_row.extend([SM['precision'], SM['recall'], SM['f1-score']])
    all_results.append(one_row)
    
results_df = pd.DataFrame(all_results, columns=['alpha', 'tn', 'fp', 'fn',
                                                'tp', 'tpr', 'tnr', 'precision',
                                                'recall', 'f1-score'])
results_df.to_csv('all_results_em.csv', sep='\t')
    
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(results_df['alpha'], results_df['f1-score'], label='f1-score')
ax1.plot(results_df['alpha'], results_df['tpr'], label='tpr')
ax1.plot(results_df['alpha'], results_df['tnr'], label='tnr')
ax1.plot(results_df['alpha'], results_df['precision'], label='precision')
ax1.plot(results_df['alpha'], results_df['recall'], label='recall')
handles, labels = ax1.get_legend_handles_labels()
lgd = ax1.legend(handles, labels)
plt.xticks (results_df['alpha'])
plt.xlabel('alpha') 
plt.show()
