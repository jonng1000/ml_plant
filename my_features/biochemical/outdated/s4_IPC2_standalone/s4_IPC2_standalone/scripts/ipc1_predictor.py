#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__webserver__ = "http://www.ipc2-isoelectric-point.org/"
__license__ = "PUBLIC DOMAIN"

# This is a simple script brought to you only for compatibility 
# It provides the access to pI predictors (18 methods) that use 
# Henderson-Hasselbach equation and pK acid dissociation constant
# The new scale has been add (IPC2_peptide) and some minor fixes 
# of the code plus speeding up by ~50% the programe (this version
# is already ultra fast, but this is crucial for IPC2 as all those
# simple models are used in it)
#
# Can use csv, fasta or plain sequence as input

import sys
import os
import math
import pickle
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from ipc2_lib.essentials import author_information
from ipc2_lib.essentials import fasta_reader
from ipc2_lib.essentials import aa_letters
from ipc2_lib.ipc import predict_isoelectric_point
from ipc2_lib.ipc import predict_isoelectric_point_ProMoST
from ipc2_lib.ipc import calculate_molecular_weight
from ipc2_lib.ipc import scales
from ipc2_lib.ipc import ipc_author_information

if __name__ == '__main__':
    
    #author_information('\t\t\t\t\t    IPC 1.0 version (optimization based)\n')
    ipc_author_information()
    available_pKa_sets = list(scales.keys())
    available_pKa_sets.append('ProMoST')
    available_pKa_sets.sort()
    
    try: 
        ipc_scale = sys.argv[1].strip()
        csv_file = sys.argv[2].strip()
        output_file = sys.argv[3].strip()
    except: 
        print("The script needs some obligatory arguments\n'python3 %s <scale> <sequences.csv/sequences.fasta/plain_seq> <output.scv>'\n"%sys.argv[0])
        print("Availabel scales: "+', '.join(available_pKa_sets)+"\n\nAdditionally, you can pass 'ALL' to calculate with all %s scales\n"%len(available_pKa_sets))
        print("e.g.\npython3 %s IPC2_peptide ../datasets/IPC2_peptide/IPC2_peptide_25.csv /tmp/pred.csv"%sys.argv[0])
        print("\npython3 %s IPC2_protein ./ipc2_lib/examples/GCA_000027325.1_ASM2732v1_protein.faa /tmp/pred.faa"%sys.argv[0]) 
        print("\npython3 %s ALL ALALAKTWKWDDDD /tmp/pred.faa\n"%sys.argv[0]) 
        sys.exit(1)
        
    input_pKa_set = ipc_scale.strip()
    if input_pKa_set not in available_pKa_sets:
        if input_pKa_set!='ALL':
            print("""Error: provided pKa set "%s" is not valid
For more information run program without arguments: python3 %s\n"""%(input_pKa_set, sys.argv[0]))
            print("Availabel scales: "+', '.join(available_pKa_sets)+"\n\nAdditionally, you can pass 'ALL' to calculate with all %s scales\n"%len(available_pKa_sets))
        
            input_pKa_set = 'ALL'
            sys.exit(1)
     
    if input_pKa_set=='ALL': scales2do = available_pKa_sets
    else: scales2do = [input_pKa_set]
    
    if input_pKa_set!='ALL':
        print('pKa used is %s: \n'%input_pKa_set)
        if input_pKa_set!='ProMoST':
            scale_str = ''
            for pKa, val in scales[input_pKa_set].items():
                scale_str += pKa+': '+str(val)+', '
            print(scale_str[:-2], '\n')
            
    #first possible input (CSV as in ../datasets/ directory)
    if csv_file.endswith('.csv'):
        validation_dataset = open(csv_file).readlines()[1:]
        print("Input file:\t"+csv_file+' (%s peptides/proteins)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)

        #validation_dataset = validation_dataset[:100]  #for testing purposes
        
        predictions = []
        Y_val = []
        validation_tab = []
        
        for line in validation_dataset:
            exp_pI, current_seq = line.split(',')
            exp_pI = float(exp_pI)
            Y_val.append(exp_pI)
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            current_seq = current_seq.strip()
            validation_tab.append([current_seq, exp_pI,])
            pI_tab = []
            for scale in scales2do:
                if scale == 'ProMoST':
                    pI = predict_isoelectric_point_ProMoST(current_seq)
                else:
                    pI = predict_isoelectric_point(current_seq, scale)
                pI_tab.append(round(pI,3))
            predictions.append(pI_tab)

        csv_str = 'exp_pI,%s,seq\n'%(','.join(scales2do))
        
        if len(scales2do)==1:
            xs = [n[0] for n in predictions]
            ys = Y_val   
            mse = mean_squared_error(ys, xs)
            msa = mean_absolute_error(ys, xs)
            rmsd = math.sqrt(mse)            
            outliers = 0
            outliers_threshold = 0.5
            for n in range(len(validation_tab)):
                csv_str += '%s,%s,%s\n'%(validation_tab[n][1], predictions[n][0], validation_tab[n][0])
                if abs(float(validation_tab[n][1])-float(predictions[n][0]))>outliers_threshold: outliers+=1
            
            perc_outliers = 100.0*outliers/len(validation_tab)
            print("\tRMSD\tMAE\tOutliers\t(%)")
            print("Test\t%.4f\t%.4f\t%s\t\t%.4f" % (rmsd, msa, outliers, perc_outliers))
        else:
            for n in range(len(validation_tab)):
                pred_str = ','.join([str(k) for k in predictions[n]])
                csv_str += '%s,%s,%s\n'%(validation_tab[n][1], pred_str, validation_tab[n][0])
        
        f = open(output_file, 'w')
        f.write(csv_str[:-1])
        f.close()

    #second possible input (FASTA as in ./ipc2_lib/examples/ directory)
    elif csv_file.endswith('.fasta') or csv_file.endswith('.faa'):
        validation_dataset = fasta_reader(csv_file)
        print("Input file:\t"+csv_file+' (%s peptides/proteins)'%str(len(validation_dataset))) 
        print('Output file:\t'+output_file+os.linesep)
        
        #validation_dataset = validation_dataset[:100]  #for testing purposes
        
        predictions = []
        validation_tab = []
        
        for query in validation_dataset:
            header, current_seq = query
            current_seq = current_seq.replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
            current_seq = current_seq.strip()
            validation_tab.append([current_seq, header]) 
            
            pI_tab = []
            for scale in scales2do:
                if scale == 'ProMoST':
                    pI = predict_isoelectric_point_ProMoST(current_seq)
                else:
                    pI = predict_isoelectric_point(current_seq, scale)
                pI_tab.append(round(pI,3))
            predictions.append(pI_tab)

        fasta_str = '>header||%s\nsequence\n'%(','.join(scales2do))
        for n in range(len(validation_tab)):
            header = validation_tab[n][1]+'||'+','.join([str(k) for k in predictions[n]])
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
            header = '>Plain sequence input'       
            validation_tab = [[seq, header]]
            #just pI as predicted by 18 methods using  Henderson-Hasselbach equation and pKp is the acid dissociation constant
            
            pI_tab = []
            predictions = []
            for scale in scales2do:
                if scale == 'ProMoST':
                    pI = predict_isoelectric_point_ProMoST(seq)
                else:
                    pI = predict_isoelectric_point(seq, scale)
                pI_tab.append(round(pI,3))
            predictions.append(pI_tab)

            print("Input sequence: "+seq)
            print('\nIsoelectric point predictions:')
            
            if len(predictions[0])>1:
                avg_pI = [n for n in predictions[0]]
                #remove Salomon
                #print(avg_pI)
                del avg_pI[-4]
                avg_pI = sum(avg_pI)/len(avg_pI)

                print(scales2do[6]+': \t'+format(predictions[0][6], '.2f'))
                print(scales2do[8]+': \t'+format(predictions[0][8], '.2f'))
                print(scales2do[5]+': \t'+format(predictions[0][5], '.2f'))
                print(scales2do[7]+': \t'+format(predictions[0][7], '.2f'))
                for n in range(0, 5):
                    print(scales2do[n]+': \t'+format(predictions[0][n], '.2f'))
                    
                for n in range(9, len(scales2do)):
                    print(scales2do[n]+': \t'+format(predictions[0][n], '.2f'))                
                print('Avg pI: \t'+format(avg_pI, '.2f'))
                
                print("\nInstructions:")
                print("\t- for protein use IPC2_protein")
                print("\t- for peptide use IPC2_peptide")  
                
            else:
                for n in range(len(scales2do)):
                    print(scales2do[n]+': \t'+format(predictions[0][n], '.2f'))                
                
            print('\nOutput file:\t'+output_file+os.linesep)    
            #print(scales2do)

            fasta_str = '>header||%s\nsequence\n'%(','.join(scales2do))
            for n in range(len(validation_tab)):
                header = validation_tab[n][1]+'||'+','.join([str(k) for k in predictions[n]])
                fasta_str += '%s\n%s\n'%(header, validation_tab[n][0])
            
            f = open(output_file, 'w')
            f.write(fasta_str[:-1])
            f.close()     
