# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:54:09 2019

@author: weixiong001

Ensemble model by varying alpha (threshold to convert average labels 
[in fractions] into 0s and 1s for individual models)
"""
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

files = [file for file in os.listdir() if 'freq_params.csv' in file]
mapping = {'dtc_freq_params.csv': 'Decision tree',
           'knn_freq_params.csv': 'k-nearest neighbors',
           'mlp_freq_params.csv': 'Multilayer perceptron',
           'rf_freq_params.csv': 'Random forest',
           'svm_freq_params.csv': 'Support-vector machine'}
names = [mapping[file] for file in files]
fig, ax = plt.subplots()
for file in files:
    df = pd.read_csv(file, sep="\t", index_col=0).reset_index(drop=True)
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Top 10 most frequent hyperparameters")
    ax.set_xticks(range(10))
    ax.set_xticklabels(list(range(1,11)))
    ax.plot(df['Freq'][:10], marker='o', markersize=5)  # Only plot first 10
    ax.legend(names)

plt.savefig("params_freq.png")


