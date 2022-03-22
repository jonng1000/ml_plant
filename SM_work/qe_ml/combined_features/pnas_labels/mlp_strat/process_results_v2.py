# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:15:58 2019

@author: weixiong001

This script is to process results from running gridsearch and SVM model
100 times. Finds average true positve rate and true negative rate from
all runs. Called v2 as it uses a different input from process_results,
it just needs all_scores.csv to analysse the scores.
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns

params_df = pd.read_csv("params_matrix.csv", sep="\t", index_col=0)
freq_params = params_df.groupby(list(params_df.columns)).size().reset_index()
freq_params.rename(columns={0: "Freq"}, inplace=True)
# Need to do this since there are many combinations of hyperparameters
#freq_params.sort_values('Freq', axis=0, ascending=False)
#   activation    alpha hidden_layer_sizes solver  Freq
#50       tanh  0.10000              (50,)    sgd     4
#23       relu  0.00001             (100,)   adam     4
#46       tanh  0.01000              (50,)    sgd     4
#44       tanh  0.00100              (50,)    sgd     4
#43       tanh  0.00100             (100,)    sgd     4
#42       tanh  0.00010              (50,)    sgd     4
#1    identity  0.00001              (50,)    sgd     3
#27       relu  0.00010              (50,)    sgd     3
#15   logistic  0.00010             (100,)  lbfgs     3
#34       relu  0.01000             (100,)    sgd     3
#35       relu  0.01000              (50,)   adam     3
#38       relu  0.10000              (50,)   adam     3
#39       relu  0.10000              (50,)    sgd     3
#41       tanh  0.00001              (50,)    sgd     3
#33       relu  0.00100              (50,)    sgd     2
#45       tanh  0.01000             (100,)    sgd     2
#32       relu  0.00100              (50,)   adam     2
#29       relu  0.00100             (100,)    sgd     2
#28       relu  0.00100             (100,)   adam     2
#47       tanh  0.10000             (100,)  lbfgs     2
#48       tanh  0.10000             (100,)    sgd     2
#24       relu  0.00001              (50,)   adam     2
#0    identity  0.00001              (50,)  lbfgs     2
#22   logistic  0.01000              (50,)  lbfgs     2
#11   identity  0.10000             (150,)    sgd     2
#19   logistic  0.01000             (100,)   adam     2
#3    identity  0.00010              (50,)    sgd     2
#8    identity  0.01000              (50,)    sgd     2
#9    identity  0.10000             (100,)    sgd     2
#49       tanh  0.10000             (150,)    sgd     1
#2    identity  0.00010              (50,)  lbfgs     1
#4    identity  0.00100             (100,)   adam     1
#5    identity  0.00100             (150,)    sgd     1
#6    identity  0.00100              (50,)    sgd     1
#7    identity  0.01000             (150,)   adam     1
#40       tanh  0.00001             (150,)    sgd     1
#10   identity  0.10000             (150,)   adam     1
#37       relu  0.10000             (100,)   adam     1
#21   logistic  0.01000             (150,)  lbfgs     1
#36       relu  0.01000              (50,)    sgd     1
#12   logistic  0.00001             (100,)  lbfgs     1
#13   logistic  0.00001              (50,)   adam     1
#14   logistic  0.00001              (50,)  lbfgs     1
#16   logistic  0.00010             (150,)  lbfgs     1
#31       relu  0.00100             (150,)    sgd     1
#30       relu  0.00100             (150,)   adam     1
#17   logistic  0.00100             (100,)  lbfgs     1
#18   logistic  0.00100             (150,)  lbfgs     1
#26       relu  0.00010              (50,)   adam     1
#20   logistic  0.01000             (100,)  lbfgs     1
#25       relu  0.00001              (50,)    sgd     1

scores_df = pd.read_csv('all_scores.csv', sep="\t", index_col=0)
# Results, not very good
scores_df['tpr'].mean()
#Out[37]: 0.5819047619047617
scores_df['tnr'].mean()
#Out[66]: 0.8797692307692313