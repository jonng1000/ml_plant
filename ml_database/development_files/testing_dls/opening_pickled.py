# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:05:36 2022

@author: weixiong001

Testing script, need to use joblib to open pickled models easily.
Checking that my original trained model and model downloaded from my website
is the same. Looks the same
"""

import pickle
from joblib import dump, load

FILE = 'agi_cluster_id_1000_direct'
FILE2 = 'agi_cluster_id_1000.pkl'
FILE3 = 'agi_cluster_id_1001.pkl'
FILE4 = 'agi_cluster_id_1.pkl'

with open(FILE, 'rb') as f:
    new_dict = pickle.load(f)
    #new_dict2 = pickle.loads(pickle.load(f))

clf = load(FILE)
clf2 = load(FILE2)
clf3 = load(FILE3)  
clf4 = load(FILE4)    

