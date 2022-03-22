#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__webserver__ = "http://www.ipc2-isoelectric-point.org/"
__license__ = "PUBLIC DOMAIN"

# The script uses SVR model for peptides (RBF, C=0.1, epsilon=0.35)
# The model is stored as pickle (../models/IPC2_peptide_75_SVR_18.pickle)
#
# The model uses only pI as predicted by 18 methods (very simple) using 
# Henderson-Hasselbach equation and pK acid dissociation constant
# adding more non-linear features did not improve and prevent convergance
#
# Can use csv, fasta or plain sequence as input

import sys
import os
import math
import pickle
import numpy as np

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import make_scorer
from sklearn.metrics import r2_score

import sklearn, time

from ipc2_lib.svr_functions import get_pI_features
from ipc2_lib.essentials import author_information
from ipc2_lib.essentials import fasta_reader
from ipc2_lib.essentials import aa_letters
    
if __name__ == '__main__':
    
    author_information('\t\t\t\t\t    (SVR version for peptides)\n')
    
    try: 
        MODEL_FILE = sys.argv[1].strip()
        csv_file = sys.argv[2].strip()
        output_file = sys.argv[3].strip()
    except: 
        print("The script needs some obligatory arguments\n'python3 %s <../models/some_model> <sequences.csv/sequences.fasta/plain_seq> <output.scv>'\n"%sys.argv[0])
        print("e.g.\npython3 %s ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_25.csv /tmp/pred.csv"%sys.argv[0])
        print("\npython3 %s ../models/IPC2_peptide_75_SVR_19.pickle ./ipc2_lib/examples/GCA_000027325.1_ASM2732v1_protein.faa /tmp/pred.faa"%sys.argv[0]) 
        print("\npython3 %s ../models/IPC2_peptide_75_SVR_19.pickle ALALAKTWKWDDDD /tmp/pred.faa\n"%sys.argv[0]) 
        
        sys.exit(1)
    
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
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            current_seq = current_seq.strip()
            validation_tab.append([current_seq, exp_pI,]) 

        #just pI as predicted by 18 methods using  Henderson-Hasselbach equation and pKp is the acid dissociation constant
        X_val,   Y_val   = get_pI_features(validation_tab)
        #make np arrays
        X_val = np.array(X_val)
        Y_val = np.array(Y_val)    

        loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
        predictions = loaded_estimator.predict(X_val)
        
        xs = predictions.tolist()
        ys = Y_val.tolist()    
        mse = mean_squared_error(ys, xs)
        msa = mean_absolute_error(ys, xs)
        rmsd = math.sqrt(mse)

        predictions = ["%.5f"%n for n in predictions.tolist()]

        csv_str = 'exp_pI,pred_pI,seq\n'
        
        outliers = 0
        outliers_threshold = 0.5
        for n in range(len(validation_tab)):
            csv_str += '%s,%s,%s\n'%(validation_tab[n][1], predictions[n], validation_tab[n][0])
            if abs(float(validation_tab[n][1])-float(predictions[n]))>outliers_threshold: outliers+=1
        
        perc_outliers = 100.0*outliers/len(validation_tab)
        #output_file = '../predictions/IPC2_peptide_25_IPC2.peptide.svr.18.csv'
        
        f = open(output_file, 'w')
        f.write(csv_str)
        f.close()
        
        print("\tRMSD\tMAE\tOutliers\t(%)")
        print("Test\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd, msa, outliers, perc_outliers))

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
            validation_tab.append([current_seq, header]) 

        #just pI as predicted by 18 methods using  Henderson-Hasselbach equation and pKp is the acid dissociation constant
        X_val,   Y_val   = get_pI_features(validation_tab)
        X_val = np.array(X_val)   
        
        loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
        predictions = loaded_estimator.predict(X_val)
        predictions = ["%.5f"%n for n in predictions.tolist()]

        fasta_str = ''
        for n in range(len(validation_tab)):
            header = validation_tab[n][1]+'||isoelectric point (IPC2 SVR peptide model): '+predictions[n]
            fasta_str += '%s\n%s\n'%(header, validation_tab[n][0])
        
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
            validation_tab = [[seq, header]]
            #just pI as predicted by 18 methods using  Henderson-Hasselbach equation and pKp is the acid dissociation constant
            X_val,   Y_val   = get_pI_features(validation_tab)
            X_val = np.array(X_val)   
            
            loaded_estimator = pickle.load(open(MODEL_FILE, 'rb'))
            predictions = loaded_estimator.predict(X_val)
            predictions = ["%.5f"%n for n in predictions.tolist()]
            
            header = '>'+header+'||isoelectric point (IPC2 SVR peptide model): '+predictions[0]
            fasta_str = '%s\n%s\n'%(header, validation_tab[0][0])
            
            print("Input sequence: "+seq)
            print('Output file:\t'+output_file+os.linesep)    
            print('Isoelectric point (IPC2 SVR peptide model): '+predictions[0])
             
            
            f = open(output_file, 'w')
            f.write(fasta_str[:-1])
            f.close()
