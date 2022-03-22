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
import os
import math
import pickle
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

from keras.models import model_from_json


from ipc2_lib.essentials import author_information 

import sklearn, time

from ipc2_lib.dl_functions import get_pKa_MLPs
    
if __name__ == '__main__':
    ######################################################################################################
    ###################################   START OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    author_information('''\t\t\t\t\t  SVR version for pKa based on MLP-SVR
                              (Multilayer Perceptron Ensemble Support Vector Regression)\n''')
    
    try: 
        train_dataset_file = sys.argv[1].strip()
        validation_dataset_file = sys.argv[2].strip()
    except: 
        print("script needs two obligatory arguments (csv format files)\n'python %s <train.csv> <validate.csv>'"%sys.argv[0])
        print("e.g. python3 %s ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../datasets/IPC2_pKa/IPC2_pKa_25.csv"%sys.argv[0])              
        sys.exit(1)

    ###################################   training data set   ############################################
    train_dataset = open(train_dataset_file).readlines()[1:]
    #print(train_dataset_file)
    #print("trainable_dataset:\t"+ str( len(train_dataset))) 
    ###################################   validation data set  ###########################################    
    validation_dataset = open(validation_dataset_file).readlines()[1:]
    #print(validation_dataset_file)
    #print("validation_dataset:\t"+ str( len(validation_dataset))) 
    
    
    ######################################################################################################
    ####################################    END OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    
    print('Training set: \t\t'+str(len(train_dataset)))
    print('Validation set: \t'+str(len(validation_dataset))) 

    path4models = '../models/'
    MODEL_files = [
    path4models+'IPC2_pKa_IPC2.pKa.seq.5mer.105',
    path4models+'IPC2_pKa_IPC2.pKa.seq.7mer.147',
    path4models+'IPC2_pKa_IPC2.pKa.seq.9mer.189',
    path4models+'IPC2_pKa_IPC2.pKa.seq.11mer.231',
    path4models+'IPC2_pKa_IPC2.pKa.seq.13mer.273',
    path4models+'IPC2_pKa_IPC2.pKa.seq.15mer.315',

    path4models+'IPC2_pKa_IPC2.pKa.seq.aaIndex.3mer.123',
    path4models+'IPC2_pKa_IPC2.pKa.seq.aaIndex.5mer.205',
    path4models+'IPC2_pKa_IPC2.pKa.seq.aaIndex.7mer.287',
    ]
    models = []
    for MODEL_FILE in MODEL_files:
        if os.path.isfile(MODEL_FILE+'.json'):
            # load json and create model
            json_file = open(MODEL_FILE+'.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            # load weights into new model
            model = model_from_json(loaded_model_json)
            model.load_weights(MODEL_FILE+".hdf5")
            print("Loaded model from disk: "+MODEL_FILE+'.json')
            model.compile(loss='mean_squared_error', optimizer='adam')
            models.append(model)
            #print(model.summary())
        else: 
            #os.system('rm '+ MODEL_FILE+'*')
            print('MODEL FILE MISSING')
            print(MODEL_FILE+'.json')
            sys.exit(1)
    
    X_train, Y_train = get_pKa_MLPs(train_dataset, models)
    X_val,   Y_val   = get_pKa_MLPs(validation_dataset, models)
    
    ROW_LENGTH = X_val.shape[-1]
    header = train_dataset_file[:-4].split('/')[-1]
    header = header.replace('/datasets/', '/models/')

    MODEL_FILE = "../models/%s_SVR_%s.pickle"%(header, ROW_LENGTH)
    
    print(MODEL_FILE)
    
    # pKa (~1s for training, just 1060 examples for training)
    # C and epsilon already optimized
    
    C_ = 10
    eps = 0.1
    print('Epsilon: '+str(eps))
    print('C: '+str(C_))
    estimator = make_pipeline(StandardScaler(), SVR(C=C_, epsilon=eps))

    estimator.fit(X_train, Y_train)
            
    # save the model to disk
    print("MODEL_FILE: "+MODEL_FILE)
    #pickle.dump(estimator, open(MODEL_FILE, 'wb'))    

    loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
    loaded_estimator = estimator
    predicted = loaded_estimator.predict(X_val)
    
    xs = predicted.tolist()
    ys = Y_val.tolist()    
    mse = mean_squared_error(ys, xs)
    mae = mean_absolute_error(ys, xs)
    rmse = mean_squared_error(ys, xs, squared=False)
    rmsd = math.sqrt(mse)
    r2 = r2_score(ys, xs)
    
    outliers = 0
    outliers_threshold = 0.5
    for n in range(len(xs)):
        if abs(xs[n]-ys[n])>outliers_threshold: outliers+=1
    perc_outliers = 100.0*outliers/len(xs)
    
    predicted = loaded_estimator.predict(X_train)

    xs = predicted.tolist()
    ys = Y_train.tolist()    
    mse2 = mean_squared_error(ys, xs)
    mae2 = mean_absolute_error(ys, xs)
    rmsd2 = mean_squared_error(ys, xs, squared=False)
    r2_2 = r2_score(ys, xs)
    outliers2 = 0
    outliers_threshold = 0.5
    for n in range(len(xs)):
        if abs(xs[n]-ys[n])>outliers_threshold: outliers2+=1
    perc_outliers2 = 100.0*outliers2/len(xs)
    
    print("\tRMSD\tMAE\tr2\tOutliers\t(%)")
    print("Train\t%.4f\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd2, mae2, r2_2, outliers2, perc_outliers2))
    print("Test\t%.4f\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd, mae, r2, outliers, perc_outliers))
