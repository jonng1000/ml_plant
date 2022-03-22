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
from ipc2_lib.dl_functions import get_ohe

def get_aaindex(aaindex_file = '../results/aaindex_feature_sel_2020_IPC2_peptide_75.csv'):
    aa_index = open(aaindex_file).readlines()
    aa_index_list = []
    for aa in aa_index:
        foo = aa.strip().split(',')
        name = foo[0]
        #print(foo)
        aa_tab = [float(n) for n in foo[2:]]
        #print(aa_tab)
        # we add X as an average (could be average weighted by % 
        # occurence of amino acids but for simplicity we do not do that
        aa_X = round(sum(aa_tab)/len(aa_tab), 2) 
        aa_tab.append(aa_X)
        aa_tab.append(0)
        
        #we normalize to (0,1)
        aa_tab = normalize(aa_tab)
        
        #AA ordering in AAindex db (X for unknown and 0 for padding)
        # A R N D C Q E G H I L K M F P S T W Y V X 0
        aa_dict = {}
        aa_names = 'A R N D C Q E G H I L K M F P S T W Y V X 0'.split()
        for n in range(0,len(aa_tab)):
            aa_dict[aa_names[n]] = aa_tab[n]            
        aa_index_list.append([name, aa_dict])
    return aa_index_list

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
                                                  SepConv2d + AvgPool\n''')
    
    try: 
        MODEL_FILE = sys.argv[1].strip()
        aaindex_file = sys.argv[2].strip()
        svr_file = sys.argv[3].strip()  
        csv_file = sys.argv[4].strip()        
        output_file = sys.argv[5].strip()
        
              
    except:
        print("The script needs some obligatory arguments\n'python3 %s <../models/some_model> <some_aaIndex> <svr.pickle> <sequences.csv/sequences.fasta/plain_seq> <output.scv>'\n"%sys.argv[0])
        print("e.g.\npython3 %s ../models/IPC2_peptide_IPC2.peptide.SepConv2D_lin2.selu.selu.selu.64.5_5.600.3_3.200.22x60 ../models/aaindex_feature_sel_2020_IPC2_peptide_75.csv ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_25.csv /tmp/pred.csv"%sys.argv[0])
        print("\npython3 %s ../models/IPC2_peptide_75_conv2d_5ch_aaindex_all_avg_softplus.relu.relu.128.5_22.50.7_7.100 ../models/aaindex_feature_sel_IPC2_peptide_75.csv ./ipc2_lib/examples/sample_peptides.faa /tmp/pred.faa"%sys.argv[0]) 
        print("\npython3 %s ../models/IPC2_peptide_75_conv2d_5ch_aaindex_all_avg_softplus.relu.relu.128.5_22.50.7_7.100 ../models/aaindex_feature_sel_IPC2_peptide_75.csv ALALAKTWKWDDDD /tmp/pred.faa\n"%sys.argv[0]) 
        sys.exit(1)

    # load json and create model
    json_file = open(MODEL_FILE+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    
    # load weights into new model
    model = model_from_json(loaded_model_json)
    model.load_weights(MODEL_FILE+".hdf5")
    print("Loaded model from disk: "+MODEL_FILE+'.json')
    #model.compile(loss='mean_squared_error', optimizer='adam')
    model.compile(loss='mean_squared_error', optimizer='adagrad')
    #print(model.summary())
            
    #first possible input (CSV as in ../datasets/ directory)
    if csv_file.endswith('.csv'):
        validation_dataset = open(csv_file).readlines()[1:]
        print("Input file:\t"+csv_file+' (%s peptides)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)

        #validation_dataset = validation_dataset[:100]  #for testing purposes
        validation_tab = []
        for line in validation_dataset:
            exp_pI, current_seq = line.split(',')
            exp_pI = float(exp_pI)
            current_seq = current_seq.strip()
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            if len(current_seq)>60:
                current_seq = truncate_seq(current_seq, 60)
            current_seq = current_seq.ljust(60, '0')
            validation_tab.append([current_seq, exp_pI,])  

        X_val,   Y_val   = get_peptide_channels(validation_tab, aaindex_file, svr_file)
        X_val = np.array(X_val)
        Y_val = np.array(Y_val) 
        
        predictions = model.predict(X_val)
        xs = [n[0] for n in predictions.tolist()]
        ys = Y_val.tolist()

        mse = mean_squared_error(ys, xs)
        msa = mean_absolute_error(ys, xs)
        rmsd = math.sqrt(mse)
        r2 = r2_score(ys, xs)
        csv_str = 'exp_pI,%s,seq\n'%MODEL_FILE.split('_')[-1]
        
        outliers = 0
        outliers_threshold = 0.25
        for n in range(len(validation_tab)):
            csv_str += '%s,%s,%s\n'%(validation_tab[n][1], predictions[n][0], validation_tab[n][0].replace('0',''))
            if abs(float(validation_tab[n][1])-float(predictions[n][0]))>outliers_threshold: outliers+=1
        
        perc_outliers = 100.0*outliers/len(validation_tab)
        #output_file = '../predictions/IPC2_peptide_25_IPC2.peptide.svr.18.csv'
        
        f = open(output_file, 'w')
        f.write(csv_str)
        f.close()
        
        print('exp_pI\tpred_pI')
        for n in range(15):
            print('%s\t%s'%(ys[n], round(xs[n], 5)))           
        
        print("\tRMSD\tMAE\tr2\tOutliers\t(%)")
        print("Test\t%.5f\t%.5f\t%.5f\t%s\t\t%.5f" % (rmsd, msa, r2, outliers, perc_outliers))

    #second possible input (FASTA as in ./ipc2_lib/examples/ directory)
    elif csv_file.endswith('.fasta') or csv_file.endswith('.faa'):
        validation_dataset = fasta_reader(csv_file)
        print("Input file:\t"+csv_file+' (%s peptides)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)
        #print(validation_dataset[:3])

        #validation_dataset = validation_dataset[:100]  #for testing purposes
        validation_tab = []
        for query in validation_dataset:
            header, current_seq = query
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            current_seq = current_seq.strip()
            if len(current_seq)>60:
                current_seq = truncate_seq(current_seq, 60)
            current_seq = current_seq.ljust(60, '0')
            validation_tab.append([current_seq, header,])  

        X_val,   Y_val   = get_peptide_channels(validation_tab, aaindex_file, svr_file)

        predictions = model.predict(X_val)
        predictions = [n[0] for n in predictions.tolist()]

        fasta_str = ''
        for n in range(len(validation_tab)):
            header = validation_tab[n][1]+'||isoelectric point (IPC2 deep learning SepConv2d peptide model): '+str(round(predictions[n],5))
            fasta_str += '%s\n%s\n'%(header, validation_tab[n][0].replace('0',''))
        
        f = open(output_file, 'w')
        f.write(fasta_str[:-1])
        f.close()    
        
    #last chance: plain AA input
    else:
        org_seq = csv_file.strip().upper()
        seq = ''.join([n for n in org_seq if n in aa_letters[:-1]])
  
        if len(seq)!=len(org_seq):
            print('The input sequence contains not allowed amino acids letter')
            print('Amino acid alphabet: '+' '.join(aa_letters[:-1]))
            print('Please, check your input')
            sys.exit(1)
        
        else:
            header = 'Plain sequence input'
            seq = seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N').strip()
            if len(seq)>60:
                seq = truncate_seq(seq, 60)
            seq = seq.ljust(60, '0')            
            
            validation_tab = [[seq, header]]
            X_val,   Y_val   = get_peptide_channels(validation_tab, aaindex_file, svr_file)

            predictions = model.predict(X_val)[0][0]
            
            header = '>'+header+'||isoelectric point (IPC2 deep learning SepConv2d peptide model): '+str(round(predictions,5))
            fasta_str = '%s\n%s\n'%(header, validation_tab[0][0].replace('0',''))
            
            print("Input sequence: "+seq.replace('0',''))
            print('Output file:\t'+output_file+os.linesep)    
            print('Isoelectric point (IPC2 deep learning SepConv2d peptide model): '+str(round(predictions,5)))
            
            f = open(output_file, 'w')
            f.write(fasta_str[:-1])
            f.close()
