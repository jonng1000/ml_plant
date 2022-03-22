#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__webserver__ = "http://www.ipc2-isoelectric-point.org/"
__license__ = "PUBLIC DOMAIN"

# The script produce model for peptides IPC2_peptide (based on >90k proteins)
# It takes two files as input, training and validation files
#
# The model of choice is SVR (sklearn)
# RBF with GridSearch had been used for find optimal seetings
# the training is quite slow (~15 min per one GridSearch iteration)
#
# The optimal C and epsilon are 1500 and 0.1293 respectively
# The model is stored as pickle
#
# the model uses only pI as predicted by 19 methods (very simple) using 
# Henderson-Hasselbach equation and pK acid dissociation constant
# adding more non-linear features did not improve and prevent convergance
#
# Tested on python3 (3.6.9), sklearn (0.24.1) and numpy (1.19.5)
# python3 ipc2_svr_peptide.py ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../datasets/IPC2_peptide/IPC2_peptide_25.csv

import sys
import math
import pickle
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

from ipc2_lib.essentials import author_information 

import sklearn, time

from ipc2_lib.svr_functions import get_pI_features
    
if __name__ == '__main__':
    ######################################################################################################
    ###################################   START OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    author_information('\t\t\t\t\t    (SVR version for peptides)\n\t\t\t\t\t\t  TRAINING SCRIPT\n')
    
    try: 
        train_dataset_file = sys.argv[1].strip()
        validation_dataset_file = sys.argv[2].strip()
    except: 
        print("script needs two obligatory arguments (csv format files)\n'python %s <train.csv> <validate.csv>'"%sys.argv[0])
        print("e.g. python3 %s ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../datasets/IPC2_peptide/IPC2_peptide_25.csv"%sys.argv[0])              
        sys.exit(1)

    ###################################   training data set   ############################################
    train_dataset = open(train_dataset_file).readlines()[1:]
    #print(train_dataset_file)
    print("trainable_dataset:\t"+ str( len(train_dataset))) 
    ###################################   validation data set  ###########################################    
    validation_dataset = open(validation_dataset_file).readlines()[1:]
    #print(validation_dataset_file)
    print("validation_dataset:\t"+ str( len(validation_dataset))) 
    
    #train_dataset = train_dataset[:200]
    #validation_dataset = validation_dataset[:100]
    ######################################################################################################
    ####################################    END OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    
    #divide trainable_dataset into two sets: training (80%), testing (20%)
    train_tab = []
    validation_tab = []
    
    for line in train_dataset:
        exp_pI, current_seq = line.split(',')
        exp_pI = float(exp_pI)
        current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
        current_seq = current_seq.strip()
        train_tab.append([current_seq, exp_pI,]) 

    for line in validation_dataset:
        exp_pI, current_seq = line.split(',')
        exp_pI = float(exp_pI)
        current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
        current_seq = current_seq.strip()
        validation_tab.append([current_seq, exp_pI,]) 
    
    #print('Training set: \t\t'+str(len(train_tab)))
    #print('Validation set: \t'+str(len(validation_tab))) 
    
    #just pI as predicted by 19 methods using  Henderson-Hasselbach equation and pKp is the acid dissociation constant
    #print('get_pI_features')
    X_train, Y_train = get_pI_features(train_tab)
    X_val,   Y_val   = get_pI_features(validation_tab)
    #print('get_pI_features')
    
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    X_val = np.array(X_val)
    Y_val = np.array(Y_val)    
    
    ROW_LENGTH = X_val.shape[-1]
    header = train_dataset_file[:-4].split('/')[-1]
    header = header.replace('/datasets/', '/models/')
    #print(header)
    
    MODEL_FILE = "../models/%s_SVR_%s.pickle"%(header, ROW_LENGTH)
    
    # peptides (~1200s for training, 90k examples for training)
    # C and gamma already optimized
    
    C_ = 1500
    eps = 0.1293
    print('Epsilon: '+str(eps))
    print('C: '+str(C_))
    estimator = make_pipeline(StandardScaler(), SVR(C=C_, epsilon=eps))

    estimator.fit(X_train, Y_train)
            
    # save the model to disk
    print("MODEL_FILE: "+MODEL_FILE)
    pickle.dump(estimator, open(MODEL_FILE, 'wb'))    

    #loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
    loaded_estimator = estimator
    predicted = loaded_estimator.predict(X_val)
    
    xs = predicted.tolist()
    ys = Y_val.tolist()    
    mse = mean_squared_error(ys, xs)
    msa = mean_absolute_error(ys, xs)
    rmsd = math.sqrt(mse)
    
    predicted = loaded_estimator.predict(X_train)

    xs = predicted.tolist()
    ys = Y_train.tolist()    
    mse = mean_squared_error(ys, xs)
    msa2 = mean_absolute_error(ys, xs)
    rmsd2 = math.sqrt(mse)

    print("\tRMSD\tMAE")
    print("Train\t%.4f\t%.4f" % (rmsd2, msa2))
    print("Test\t%.4f\t%.4f" % (rmsd, msa))
