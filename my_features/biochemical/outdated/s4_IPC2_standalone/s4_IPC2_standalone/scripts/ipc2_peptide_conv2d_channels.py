#!/usr/bin/python3

# this script will construct csv file suitable for TensorFlow and run training

import sys
import os
import random
import string
import math
import random
import pickle
import numpy as np

import keras
import tensorflow as tf
from keras.utils import plot_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout, Flatten, Activation, Reshape, BatchNormalization, Convolution2D, AveragePooling2D, SeparableConv2D 
from keras.callbacks import ModelCheckpoint, EarlyStopping, RemoteMonitor, Callback
from keras.models import model_from_json

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

from ipc2_lib.essentials import author_information, normalize
from ipc2_lib.essentials import aa_letters
from ipc2_lib.essentials import get_hydrophobicity

from ipc2_lib.ipc import predict_isoelectric_point
from ipc2_lib.ipc import predict_isoelectric_point_ProMoST
from ipc2_lib.ipc import calculate_molecular_weight
from ipc2_lib.ipc import scales

from ipc2_lib.dl_functions import seq2ohe
from ipc2_lib.dl_functions import get_ohe, get_aaindex

def get_peptide_channels(dataset_tab, aaindex_file, svr_file):
    
    #15 features
    aaindex_list = get_aaindex(aaindex_file)
    
    #19 features (+ProMoST)
    available_pKa_sets = list(scales.keys())
    available_pKa_sets.sort()
    
    #load SVR model (once)
    loaded_estimator = pickle.load(open(svr_file, 'rb'))
    
    features2d = []   #X
    labels = []     #Y
    prot_counter = 0
    for query in dataset_tab:
        prot_counter+=1
        if prot_counter%5000==0: print(prot_counter)
        single_sequence, score = query
        seq_len = len(single_sequence)
        org_single_sequence = single_sequence.replace('0','')
        
        #===================== channel 1 =========================
        # one-hot-encoded org_single_sequence
        
        #22x60 (ohe defines "image" shape)
        ch1 = np.array(seq2ohe(single_sequence))
        
        #===================== channel 2 =========================
        # features from aaIndex
        
        features = []
        for aaindex in aaindex_list:
            aa_tab = []
            for n in range(0, len(single_sequence)):
                aa_tab.append(aaindex[1][single_sequence[n]])
            features.append(aa_tab)
            
        #hydrophobicity (K&D) - padding extension by 0.0 !!!
        kd_tab = get_hydrophobicity(org_single_sequence)
        len_diff = seq_len-len(kd_tab) 
        kd_tab += len_diff*[0.0]
        features.append(kd_tab)
        
        #this defines 2nd channel thus we fill up 6 rows with 0 
        features.append([0]*seq_len)
        features.append([0]*seq_len)
        features.append([0]*seq_len)
        features.append([0]*seq_len)
        features.append([0]*seq_len)
        features.append([0]*seq_len)

        ch2 = np.array(features)
        
        #===================== channel 3 =========================        
        # counts of all amino acids
        
        features = []
        for aa in aa_letters:
            features.append([single_sequence.count(aa)]*seq_len)
            
        ch3 = np.array(features)
        
        #===================== channel 4 ========================= 
        # predictions of pI
        
        features = []
        pI_tab2 = []
        # predict_isoelectric_point as predicted in IPC 1.0
        for scale in available_pKa_sets:
            pI = round(predict_isoelectric_point(org_single_sequence, scale), 5)
            pI_tab = [pI]*seq_len
            pI_tab2.append(pI)
            features.append(pI_tab)
        
        #extra pI from ProMoST (72 param model)
        pI = round(predict_isoelectric_point_ProMoST(org_single_sequence), 5)        
        pI_tab = [pI]*seq_len
        pI_tab2.append(pI)
        features.append(pI_tab)
        
        #pI from svr
        pI_val = np.array([pI_tab2])
        pI = round(loaded_estimator.predict(pI_val).tolist()[0],5)
        pI_tab = [pI]*seq_len
        features.append(pI_tab)
        
        #this defines 4th channel thus we fill up 2 rows with 0 
        features.append([0]*seq_len)
        features.append([0]*seq_len)
        #features.append(pI_tab)
        #features.append(pI_tab)
        
        ch4 = np.array(features)

        #===================================================
        
        #arrange all channels
        ch14 = np.dstack([ch1,ch2,ch3,ch4])
        
        labels.append(score)
        features2d.append(ch14)
        
    X = np.array(features2d)
    Y = np.array(labels)
    
    return X, Y

def truncate_seq(current_seq, limit = 3000):
    '''truncate too long protein'''
    # remove randomly selected non-charged residues
    # this should be relatively save approach
    # 3k aa have only 0.18826% of proteins in UniRef
    # charged residues constitute 30.535 of aa
    # thus removing charged residues 
    to_remove = len(current_seq)-limit
    if to_remove<=0: return current_seq
    indexes = list(range(0, len(current_seq)))
    acidic = ['D', 'E', 'C', 'Y']
    basic = ['K', 'R', 'H']
    charged_aa = acidic + basic
    random.shuffle(indexes)
    to_del_list = []
    for inx in indexes:
        if current_seq[inx] not in charged_aa:
            to_del_list.append(inx)
            to_remove -= 1
        if to_remove==0:
            break
    
    #print('Indexes to remove:', to_del_list)
    new_seq = ''
    for n in range(0, len(current_seq)):
        if n not in to_del_list:
            new_seq+=current_seq[n]
    if to_remove==0:
        #print('Success')
        pass
    else:
        # 30% of charged and 3k limit means that this occurs when 
        # protein has over 10k aa and such proteins are extremely 
        # rare (0.00416% (10,858 proteins out of 261M)
        print("Still too much, extremly long sequence")
        print(new_seq)
        new_seq = new_seq[:limit]
    return new_seq

if __name__ == '__main__':
    ######################################################################################################
    ###################################   START OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    author_information('''
                                          deep learning version for peptides
                                                        60x22x4 
                                              (2D vector with 4 channels)
                                                  SepConv2d + AvgPool
                                                    TRAINING SCRIPT\n''')
    
    try: 
        train_dataset_file = sys.argv[1].strip()
        validation_dataset_file = sys.argv[2].strip()
        aaindex_file = sys.argv[3].strip()
        svr_file = sys.argv[4].strip()
    except: 
        print("script need three obligatory arguments \ne.g. 'python %s <train.csv> <validate.csv> <aaindex.csv> <svr.pickle>'"%sys.argv[0])
        sys.exit(1)
    

    ###################################   training data set   ############################################
    train_dataset = open(train_dataset_file).readlines()[1:]
    print(train_dataset_file)
    #print("trainable_dataset:\t"+ str( len(train_dataset))) 
    
    random.shuffle(train_dataset)
    
    ###################################   validation data set  ###########################################    
    validation_dataset = open(validation_dataset_file).readlines()[1:]
    print(validation_dataset_file)
    #print("validation_dataset:\t"+ str( len(validation_dataset))) 
    
    # for testing only
    #train_dataset = train_dataset[:300]
    #validation_dataset = validation_dataset[:50]
    ######################################################################################################
    ####################################    END OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    
    random.shuffle(train_dataset)
    
    train_tab = []
    validation_tab = []

    for line in train_dataset:
        exp_pI, current_seq = line.split(',')
        exp_pI = float(exp_pI)
        #frist of all we add 60aa limit and fill by zeros
        current_seq = current_seq.strip()
        current_seq = current_seq.ljust(60, '0')[:60]
        current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
        train_tab.append([current_seq, exp_pI,]) 

    for line in validation_dataset:
        exp_pI, current_seq = line.split(',')
        exp_pI = float(exp_pI)
        current_seq = current_seq.strip()
        current_seq = current_seq.ljust(60, '0')[:60]
        current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
        validation_tab.append([current_seq, exp_pI,]) 
    
    print('Training set: \t\t'+str(len(train_tab)))
    print('Validation set: \t'+str(len(validation_tab))) 
    #print(validation_tab[0], len(validation_tab[0]))
      
    X_train, Y_train = get_peptide_channels(train_tab, aaindex_file, svr_file)
    X_val,   Y_val   = get_peptide_channels(validation_tab, aaindex_file, svr_file)
    
    #print(X_train.shape)
    
    shape_tab = X_val.shape
    
    ROW_LENGTH = X_val.shape[-2]
    ROW_LENGTH2 = X_val.shape[-3]
    #================================================= 
    des = 'selu selu selu 64 22_5 50 3_3 400'
    #des = 'selu selu selu 64 5_5 200 3_3 600'
    MODEL_FILE = "../models/IPC2_peptide_IPC2.peptide.SepConv2D_Adam___%s.%sx%s"%(des.replace(' ', '.'), ROW_LENGTH2, ROW_LENGTH)
    print(des)
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
    
    else: 
        #os.system('rm '+ MODEL_FILE+'*')
        print('Training new model: '+MODEL_FILE)
        ####################################################################################
        ###                               ML model                                       ###
        ####################################################################################  


        ##AveragePooling2D   much more complicated. division, thus floats
        ##MaxPooling2D       much faster as it works on int with max
        
        a1 = des.split()[0]
        a2 = des.split()[1]
        a3 = des.split()[2]
        BATCH_SIZE = int(des.split()[3])
        fs1_1 = int(des.split()[4].split('_')[0])
        fs1_2 = int(des.split()[4].split('_')[1])
        f1 = int(des.split()[5])
        fs2_1 = int(des.split()[6].split('_')[0])
        fs2_2 = int(des.split()[6].split('_')[1])
        f2 = int(des.split()[7])    
        
        model = Sequential()
        model.add(SeparableConv2D(f1, (fs1_1, fs1_2), padding='same', input_shape=shape_tab[1:], activation=a1))
        model.add(AveragePooling2D(pool_size=(2, 4)))
        model.add(SeparableConv2D(f2, (fs2_1, fs2_2), padding='same', activation=a2))
        model.add(AveragePooling2D(pool_size=(1, 3))) 
        model.add(Flatten())
        model.add(Dense(units = 60, activation = a3))
        model.add(Dense(units = 60, activation = a3))
        #model.add(Dropout(0.2))
        model.add(Dense(units = 60, activation = a3))        
        model.add(Dense(units = 1, kernel_initializer='normal', activation="linear"))

        print(model.summary())
        
        #print(kk)
        # Compile model
        print ('Compiling model...')        
        model.compile(loss='mean_squared_error', optimizer='adam')

        # serialize model to JSON
        model_json = model.to_json()
        with open(MODEL_FILE+".json", "w") as json_file:
            json_file.write(model_json)         
        #sys.exit(1)
        OPTIMIZER = 'adam'
        #OPTIMIZER = 'adagrad'
        print('Optimizer: '+OPTIMIZER) 
        
        checkpointer = ModelCheckpoint(filepath=MODEL_FILE+'.hdf5', verbose=1, save_best_only=True)
        checkpointer2 = EarlyStopping(monitor='val_loss', patience=20)
        NB_EPOCH = 120
        #BATCH_SIZE = 128
        model.fit(X_train, Y_train, 
                epochs=NB_EPOCH, 
                batch_size=BATCH_SIZE,
                validation_split=0.2,
                callbacks=[checkpointer, checkpointer2],
                verbose=1
                )

        model.save_weights(MODEL_FILE+".hdf5")
        #plot_model(model, to_file=MODEL_FILE+'.png')
    
    #print(X_val)
    #print(X_val.shape)
        
    predicted = model.predict(X_train)
    xs = [n[0] for n in predicted.tolist()]
    ys = Y_train.tolist()
    mse = mean_squared_error(ys, xs)
    msa2 = mean_absolute_error(ys, xs)
    rmsd2 = math.sqrt(mse)
    r2_2 = r2_score(ys, xs)
    outliers2 = 0
    outliers_threshold = 0.25
    for n in range(len(xs)):
        if abs(xs[n]-ys[n])>outliers_threshold: outliers2+=1
    perc_outliers2 = 100.0*outliers2/len(xs)
    
    predicted = model.predict(X_val)
    xs = [n[0] for n in predicted.tolist()]
    ys = Y_val.tolist()    
    mse = mean_squared_error(ys, xs)
    msa = mean_absolute_error(ys, xs)
    rmsd = math.sqrt(mse)
    r2 = r2_score(ys, xs)
    outliers = 0
    outliers_threshold = 0.25
    for n in range(len(xs)):
        if abs(xs[n]-ys[n])>outliers_threshold: outliers+=1
    perc_outliers = 100.0*outliers/len(xs)
    
    print("\tRMSD\tMAE\tr2\tOutliers\t(%)")
    print("Train\t%.4f\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd2, msa2, r2_2, outliers2, perc_outliers2))
    print("Test\t%.4f\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd, msa, r2, outliers, perc_outliers))
    
    
