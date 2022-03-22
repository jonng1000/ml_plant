import os, sys, math

from scipy import mean
import numpy as np

import statistics

from sklearn.model_selection import RepeatedKFold
import numpy as np

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

def get_predictions(prediction_file, outliers_threshold = 0.50, set_number = 25):
    lines = open(prediction_file).readlines()[1:]
    y = [float(n.split(',')[0]) for n in lines]
    X = [[float(n.split(',')[1])] for n in lines]
    print(len(y), len(X), prediction_file)
    #print(prediction_file)    
    X = np.array(X)
    y = np.array(y)
    
    #this is 10-fold CV repeated 10 times(!)
    rkf = RepeatedKFold(n_splits=10, n_repeats=10, random_state=None)
    
    counter = 1
    mean_mse = []
    mean_rmsd = []
    mean_mae = []
    mean_r2 = []
    mean_adj_r2 = []
    mean_outliers = []
    #print(prediction_file)
    #print(len(X))
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        xs = X_test.tolist()
        xs = [n[0] for n in xs]
        ys = y_test.tolist()
        outliers = 0
        for n in range(len(xs)):
            if abs(xs[n]-ys[n])>outliers_threshold: outliers+=1 
        mean_outliers.append(outliers)
        
        mse = mean_squared_error(ys, xs)
        mse = mean_squared_error(ys, xs)
        mae = mean_absolute_error(ys, xs)
        
        rmsd = math.sqrt(mse)
        #print(mse, rmsd)
        mean_mse.append(mse)
        mean_rmsd.append(rmsd)
        r2 = r2_score(ys, xs)
        adj_r2 = 1-(1-r2)*(len(xs)-1)/(len(xs)-1-1)
        mean_r2.append(r2)
        mean_adj_r2.append(adj_r2)
        mean_mae.append(mae)
        #print(r2_score(ys, xs))
        counter+=1
    
    method = prediction_file.split('_'+str(set_number)+'_')[1][:-4]
    
    return method, round(statistics.mean(mean_rmsd),5), round(statistics.mean(mean_mae),5), round(statistics.mean(mean_r2),5), int(sum(mean_outliers)/10)
    
if __name__ == '__main__':   
    try: 
        dataset = sys.argv[1].strip()
        supp_type = sys.argv[2].strip()
    except: 
        print("The script needs two arguments\nDataset: IPC2_peptide_25 / IPC2_peptide_75 / IPC2_protein_25 / IPC2_protein_75 / IPC2_pKa_25 \nType of the table: main / supp \n\ne.g. 'python3 %s IPC2_peptide_25 main'\n"%sys.argv[0])
        print("For pKa table from supplement run: 'python3 calculate_table_stats.py IPC2_pKa_25 supp'")
        sys.exit(1)
    
    try:
        print_columns = int(sys.argv[3].strip())
    except:
        print_columns = 0
        
    csv_db_path = '../predictions/'
    predictions_tab = os.listdir(csv_db_path)
    #print(predictions_tab)
    
    print('\n\nResults for: '+dataset+'\n')  
    
    #initial cleaning 
    predictions_tab = [n for n in predictions_tab if n.endswith('.csv')]  
    
    #only those of interest
    predictions_tab = [csv_db_path+n for n in predictions_tab if n.startswith(dataset)]
    
    #print(predictions_tab)
    #print(kk)
    
    dataset_type = int(dataset.split('_')[-1])
    
    #limit to main or suppl
    #this works only for very specific naming 
    #need to change the lists if neccessary
    if 'peptide' in dataset:
        outlier_threshold = 0.25
        if supp_type=='supp':
            to_keep = ['IPC2.peptide.svr.19', 'IPC2.peptide1320', 'IPC2.peptide.Conv2D',
                       'IPC2.peptide19', 'Bjellqvist', 'IPC_peptide', 'IPC2_peptide']
        else: 
            to_keep = ['PredpI-TMT6', 'Grimsley', 'Thurlkill', 'Solomon', 'IPC2.peptide.svr.19', 'IPC2.peptide.Conv2D', 'Sillero', 'IPC_protein', 'ProMoST', 
                       'Toseland', 'DTASelect', 'Wikipedia', 'Lehninger', 'IPC_peptide', 'Nozaki', 'Patrickios', 'Rodwell', 
                        'IPC2_peptide', 'PredpI-iTRAQ8', 'EMBOSS', 'PredpI-plain', 'pIR', 'Bjellqvist', 'Dawson', 'IPC2_protein']
    elif 'pKa' in dataset:
        outlier_threshold = 0.5
        if supp_type=='supp':
            #to_keep = [
                       #'IPC2.aaIndex3', 'IPC2.aaIndex5','IPC2.aaIndex7',
                       #'IPC2.aaIndex9', 'IPC2.aaIndex11',
                       #'IPC2.seq3', 'IPC2.seq5','IPC2.seq7','IPC2.seq9',
                       #'IPC2.seq11', 'IPC2.seq13','IPC2.seq15',
                       #'IPC2.seq3.aaIndex.3','IPC2.seq5.aaIndex.5',
                       #'IPC2.seq7.aaIndex.7','IPC2.seq9.aaIndex.9',
                       #'IPC2.seq11.aaIndex.11', 'IPC2.seq13.aaIndex.13' 
                       #'IPC2.seq13.aaIndex5', 'IPC2.mlp-svr.9',
                       #]
            to_keep = [            
                       'Gray_IPC2.aaIndex3', 'Gray_IPC2.aaIndex5', 'Gray_IPC2.aaIndex7',
                       'Gray_IPC2.aaIndex9', 'Gray_IPC2.aaIndex11','Gray_IPC2.seq3',
                       'Gray_IPC2.seq5',     'Gray_IPC2.seq7',     'Gray_IPC2.seq9',
                       'Gray_IPC2.seq11',    'Gray_IPC2.seq13',    'Gray_IPC2.seq15',
                       'Gray_IPC2.seq3.aaIndex3',   'Gray_IPC2.seq5.aaIndex5',
                       'Gray_IPC2.seq7.aaIndex7',   'Gray_IPC2.seq9.aaIndex9',
                       'Gray_IPC2.seq11.aaIndex11', 'Gray_IPC2.seq13.aaIndex13',
                       'Gray_IPC2.seq13.aaIndex5',   'Gray_IPC2.mlp-svr.9', 
                       'Gray_ensemble_avg', 'Gray_neighbour_repack',
                       'Gray_site_repack', 'Gray_std_rosseta',
                        ]
            
        if supp_type=='main':
            to_keep = [            
                       'Gray_IPC2.mlp-svr.9', 
                       'Gray_ensemble_avg', 'Gray_neighbour_repack',
                       'Gray_site_repack', 'Gray_std_rosseta',
                        ]
    else:
        outlier_threshold = 0.5
        if supp_type=='supp':
            to_keep = ['IPC_protein', 'IPC2.protein.svr.19', 'ProMoST',  'IPC2_protein']
        else:
            to_keep = ['Bjellqvist', 'EMBOSS', 'IPC_protein', 'IPC2.protein.svr.19', 'Lehninger', 'PredpI-TMT6', 'Toseland', 'DTASelect',
                       'Sillero', 'Wikipedia', 'Solomon', 'Nozaki', 'Rodwell', 'Grimsley', 'Thurlkill', 'Dawson', 'pIR', 'PredpI-iTRAQ8',
                       'PredpI-plain', 'Patrickios', 'ProMoST', 'IPC2_protein']
    #print(to_keep)
    to_keep = [str(dataset_type)+'_'+n for n in to_keep]
    #print(to_keep)
    #print(str(dataset_type))
    
    tmp_tab = []
    for dataset_file in predictions_tab:
        for keeper in to_keep:
            if keeper+'.csv' in dataset_file:
                tmp_tab.append(dataset_file)
    predictions_tab = tmp_tab
    
    prediction_results_tab = []
    for prediction_file in predictions_tab:
        method, rmse, mae, r2, outliers = get_predictions(prediction_file, outlier_threshold, dataset_type)
        prediction_results_tab.append([rmse, mae, r2, outliers, method])
        
    prediction_results_tab.sort(key=lambda x:x[0])
    print('\nOutlier_threshold:', outlier_threshold)
    print('\n'+'The results are 10-fold CV-ed thus they may differ a little bit from run to run'.upper()+'\n') 
    print('RMSD\tMAE\t r2\tOutliers\tMethod')
    for result in prediction_results_tab:
        if result[2]<0:
            print(format(result[0], '.4f')+'\t'+format(result[1], '.4f')+'\t'+format(result[2], '.4f')+'\t'+str(int(result[3]))+'\t\t'+result[4].replace('Gray_',''))
        else:
            print(format(result[0], '.4f')+'\t'+format(result[1], '.4f')+'\t '+format(result[2], '.4f')+'\t'+str(int(result[3]))+'\t\t'+result[4].replace('Gray_',''))
    
    if print_columns:
        print('\n=============================\n')
        print('Produce the whole columns of table')
        print('\n'+dataset+' Methods')
        for result in prediction_results_tab:
            print(result[-1].replace('Gray_',''))    
            
        print('\n\n'+dataset+' RMSE')
        for result in prediction_results_tab:
            print("%.4f" % result[0])    
            
        print('\n\n'+dataset+' MAE')
        for result in prediction_results_tab:
            print("%.4f" % result[1]) 
            
        print('\n\n'+dataset+' r2')
        for result in prediction_results_tab:
            print("%.4f" % result[2])     
            
        print('\n\n'+dataset+' outliers')
        for result in prediction_results_tab:
            print(result[3])           

