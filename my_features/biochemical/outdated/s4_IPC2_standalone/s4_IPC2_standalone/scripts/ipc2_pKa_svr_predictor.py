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

from keras.models import model_from_json

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

from ipc2_lib.essentials import author_information 
from ipc2_lib.essentials import aa_letters
from ipc2_lib.essentials import fasta_reader

from ipc2_lib.dl_functions import find_charged
from ipc2_lib.dl_functions import get_kmers
from ipc2_lib.dl_functions import get_pKa_MLPs


if __name__ == '__main__':
    ######################################################################################################
    ###################################   START OF PROCESSING INPUT PARAMETERS    ########################
    ######################################################################################################
    author_information('''\t\t\t\t\t  SVR version for pKa based on MLP-SVR
                              (Multilayer Perceptron Ensemble Support Vector Regression)\n''')
    
    try: 
        MODEL_FILE = sys.argv[1].strip()
        csv_file = sys.argv[2].strip()
        output_file = sys.argv[3].strip()
    except: 
        print("The script needs some obligatory arguments\n'python3 %s <SVR.pickle> <sequences.csv/sequences.fasta/plain_seq> <output.scv>'\n"%sys.argv[0])
        print("e.g.\npython3 %s ../models/IPC2_pKa_75_SVR_9.pickle ../datasets/IPC2_pKa/IPC2_pKa_25.csv /tmp/pred.csv"%sys.argv[0])
        print("\npython3 %s ../models/IPC2_pKa_75_SVR_9.pickle ./ipc2_lib/examples/GCA_000027325.1_ASM2732v1_protein.faa /tmp/pred.faa"%sys.argv[0]) 
        print("\npython3 %s ../models/IPC2_pKa_75_SVR_9.pickle ALALAKTWKWDDDD /tmp/pred.faa\n"%sys.argv[0]) 
        print('\nNote:')
        print('\tIf csv used it need to have specific structure (see the example file)')
        sys.exit(1)
    
    validation_tab = []
    mer = 15
    tail = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    tail_len = len(tail)
    half_mer = int((mer-1)/2)
    
    #load MLP models
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
    for DL_MODEL_FILE in MODEL_files:
        if os.path.isfile(DL_MODEL_FILE+'.json'):
            # load json and create model
            json_file = open(DL_MODEL_FILE+'.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            # load weights into new model
            model = model_from_json(loaded_model_json)
            model.load_weights(DL_MODEL_FILE+".hdf5")
            print("Loaded model from disk: "+DL_MODEL_FILE+'.json')
            model.compile(loss='mean_squared_error', optimizer='adam')
            models.append(model)
            #print(model.summary())
        else: 
            #os.system('rm '+ DL_MODEL_FILE+'*')
            print('MODEL FILE MISSING')
            print(DL_MODEL_FILE+'.json')
            sys.exit(1)    
    #load SVR model from pickle
    loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
    
    #first possible input (CSV as in ../datasets/ directory)
    if csv_file.endswith('.csv'):
        validation_dataset = open(csv_file).readlines()[1:]
        print("Input file:\t"+csv_file+' (%s pKa values)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)
    
        #pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,sequence
        validation_tags = []
        for line in validation_dataset:
            pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,current_seq = line.split(',')
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            exp_pKa = float(pKa)
            current_seq = tail + current_seq.strip() + tail
            kmer = current_seq[int(position)-(half_mer+1)+len(tail):int(position)+half_mer+len(tail)]
            validation_tab.append([kmer, exp_pKa,])
            pdb_chain_pos_aa_kmer = '_'.join([pdb,chain,position,aa,kmer])
            validation_tags.append(pdb_chain_pos_aa_kmer)        
        
        #print(validation_dataset[:2])
        #print(kk)
        X_val,   Y_val   = get_pKa_MLPs(validation_dataset, models)
        
        predictions = loaded_estimator.predict(X_val)
        
        xs = predictions.tolist()
        ys = Y_val.tolist() 
        
        mse = mean_squared_error(ys, xs)
        msa = mean_absolute_error(ys, xs)
        rmsd = math.sqrt(mse)
        r2 = r2_score(ys, xs)
        outliers = 0
        outliers_threshold = 0.5
        csv_str = 'exp_pKa,MLP-SVR-model,kmer\n'
        for n in range(len(xs)):
            if abs(xs[n]-ys[n])>outliers_threshold: outliers+=1
            csv_str += '%s,%s,%s\n'%(validation_tab[n][1], round(xs[n],5), validation_tags[n])
        perc_outliers = 100.0*outliers/len(xs)
    
        print("\tRMSD\tMAE\tr2\tOutliers\t(%)")
        print("Test\t%.4f\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd, msa, r2, outliers, perc_outliers))
        
        f = open(output_file, 'w')
        f.write(csv_str)
        f.close()
        
    #second possible input (FASTA as in ./ipc2_lib/examples/ directory)
    elif csv_file.endswith('.fasta') or csv_file.endswith('.faa'):
        validation_dataset = fasta_reader(csv_file)
        tmp_val = []
        ch_tab = ['D', 'E', 'Y', 'H', 'K']
        for n in range(len(validation_dataset)):
            seq = validation_dataset[n][1]
            if seq[0] in ch_tab: seq = 'A'+seq
            if seq[-1] in ch_tab: seq = seq+'A'
            seq = tail+seq+tail
            tmp_val.append([validation_dataset[n][0], seq])
            
        validation_dataset = [[n[0], tail+n[1]+tail] for n in validation_dataset]
        validation_dataset = tmp_val
        print("Input file:\t"+csv_file+' (%s proteins/peptides)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)

        fasta_str = ''
        pKa_pred_counter = 0
        for n in range(len(validation_dataset)):
            full_seq = validation_dataset[n][1]
            full_seq = full_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N').strip()
                
            validation_tab = find_charged(full_seq, n, tail_len, half_mer)
            #print(validation_tab, len(validation_tab))
            
            #pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,current_seq = line.split(',')
            deep_validation_tab = []
            for kmer2do in validation_tab:
                tmp_kmer = kmer2do[0]
                dummy_csv_line = '0,0,0,0,%s,%s,%s,'%(kmer2do[1][1], 8, kmer2do[1][1])
                dummy_csv_line += tmp_kmer[6:9]+','  #trimer
                dummy_csv_line += tmp_kmer[5:10]+',' #pentamer
                dummy_csv_line += tmp_kmer[4:11]+',' #heptamer
                dummy_csv_line += tmp_kmer[3:12]+',' #nonamer
                dummy_csv_line += tmp_kmer+'\n'
                deep_validation_tab.append(dummy_csv_line)
            print("Protein %s/%s: %s pKa predicted"%(n+1, len(validation_dataset), len(deep_validation_tab)))
            #print(deep_validation_tab[:2])
            X_val,   Y_val   = get_pKa_MLPs(deep_validation_tab, models)
            predictions = loaded_estimator.predict(X_val)
            xs = predictions.tolist()
            pKa_pred_counter += len(predictions)
            pKa_str = ''
            for j in range(len(validation_tab)):
                pKa_str += validation_tab[j][1][1]+str(validation_tab[j][1][2])+'_'+str(round(predictions[j],5))+';'
            
            header = validation_dataset[n][0]+'||pseudo-fasta format (extra line with pKa predictions from MLP-SVR-model)'
            org_seq = validation_dataset[n][1]
            org_seq = org_seq[tail_len:-tail_len]
            fasta_str += '%s\n%s\n%s\n'%(header, org_seq, pKa_str[:-1])
        
        f = open(output_file, 'w')
        f.write(fasta_str[:-1])
        f.close()      
        
        print('Number of pKa predicted: '+str(pKa_pred_counter))
        
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
            header = '>Plain sequence input'
            seq = seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            full_seq = tail+seq+tail   
            validation_tab = find_charged(full_seq, 0, tail_len, half_mer)
            fasta_str = ''
            pKa_pred_counter = 0

            #pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,current_seq = line.split(',')
            deep_validation_tab = []
            for kmer2do in validation_tab:
                tmp_kmer = kmer2do[0]
                dummy_csv_line = '0,0,0,0,%s,%s,%s,'%(kmer2do[1][1], 8, kmer2do[1][1])
                dummy_csv_line += tmp_kmer[6:9]+','  #trimer
                dummy_csv_line += tmp_kmer[5:10]+',' #pentamer
                dummy_csv_line += tmp_kmer[4:11]+',' #heptamer
                dummy_csv_line += tmp_kmer[3:12]+',' #nonamer
                dummy_csv_line += tmp_kmer+'\n'
                deep_validation_tab.append(dummy_csv_line)
            #print(deep_validation_tab)
            #print(len(deep_validation_tab))
            X_val,   Y_val   = get_pKa_MLPs(deep_validation_tab, models)
            predictions = loaded_estimator.predict(X_val)
            xs = predictions.tolist()
            pKa_pred_counter += len(predictions)
            pKa_str = ''
            for j in range(len(validation_tab)):
                pKa_str += validation_tab[j][1][1]+str(validation_tab[j][1][2])+'_'+str(round(predictions[j],5))+';'
            
            header = header+'||pseudo-fasta format (extra line with pKa predictions from MLP-SVR-model)'
            fasta_str += '%s\n%s\n%s\n'%(header, seq, pKa_str[:-1])
        
            f = open(output_file, 'w')
            f.write(fasta_str[:-1])
            f.close()      
                
            print('Number of pKa predicted: '+str(pKa_pred_counter))  
            
            print(pKa_str[:-1].split(';'))
            
