import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

#protData = 'anthonyNormalized.txt'
protData = 'imputed_anthonyFormatted.txt'

### Reading in the raw proteomic data
#data = pd.read_csv('imputed.txt', sep='\t', index_col=0, usecols = [0,3,4,5,6,7,8,9,11]) #raw
data = pd.read_csv(protData, sep='\t', index_col=0) #Antony's average
###replacing missing data with the column average


### Reading in the gold standard data
gold = pd.read_csv('goldStandard.txt', sep='\t')
### Anthony left some duplicates in there, need to remove
gold.sort_values("Gene", inplace = True) 
gold.drop_duplicates(subset ="Gene", keep = 'first', inplace = True)
gold = gold.set_index('Gene')

### Getting genes that are in raw and gs data, then getting the corresponding prot data
commonGenes = list(set(data.index)&set(gold.index))

### Since in proteomic data many genes are found multiple times (3 bio replicates), labels from gold need to be also replicated
genes = data.loc[commonGenes,:] #getting the proteomic data of genes in gold standard
labels = []
for gene in genes.index:
    labels.append(list(gold.loc[gene,:])) #getting the corresponding labels (i.e. localications) from gold
labels = pd.DataFrame(labels, columns = gold.columns)  #making a proper dataframe

save = []
for label in labels:
    curLabels = labels[label] # gets labels for a current compartment
    X_train, X_test, y_train, y_test = train_test_split(genes, curLabels, test_size=0.2, stratify=curLabels) #splitting it into train and test, stratify makes sure that there are always 1s
    
    #Parameters for grid search
    ###remember to add svm__ in front of the parameters. It needs to match the pipeline ('svm', SVC())!!!!
    par_svm = [{'svm__kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'svm__gamma': [1e-5,1e-4,1e-3,1e-2,1e-1,'auto'],'svm__C': [1, 10, 100, 1000]}]
    par_knn = [{'knn__n_neighbors':  list(range(2,21,2)), 'knn__weights' : ['uniform', 'distance'], "knn__leaf_size" : [3,10,30,60]}]
    par_dcc = [{'dcc__max_depth': list(range(10, 251,5))+[None], "dcc__min_samples_split": range(2, 10)}]
    par_mlp = [{'mlp__solver': ['lbfgs', 'sgd', 'adam'], 'mlp__activation' : ['identity', 'logistic', 'tanh', 'relu'], "mlp__alpha": [1e-5,1e-4,1e-3,1e-2,1e-1], "mlp__hidden_layer_sizes":(500, 50)}]
    par_rfc = [{'rfc__max_depth': list(range(5, 50,10))+[None],"rfc__n_estimators": [2,5,10,20,50], "rfc__min_samples_split": range(2, 10)}]
    
#    Parameters for grid search
    if protData == 'imputed_anthonyFormatted.txt':
        pipe_svm = Pipeline([('scl', StandardScaler()), ('svm', SVC())])
        pipe_knn = Pipeline([('scl', StandardScaler()), ('knn', KNeighborsClassifier())])
        pipe_dcc = Pipeline([('scl', StandardScaler()), ('dcc', DecisionTreeClassifier())])
        pipe_mlp = Pipeline([('scl', StandardScaler()), ('mlp', MLPClassifier(max_iter=10000))])
        pipe_rfc = Pipeline([('scl', StandardScaler()), ('rfc', RandomForestClassifier())])
    if protData == 'anthonyNormalized.txt':    
        pipe_svm = Pipeline([('svm', SVC())])
        pipe_knn = Pipeline([('knn', KNeighborsClassifier())])
        pipe_dcc = Pipeline([('dcc', DecisionTreeClassifier())])
        pipe_mlp = Pipeline([('mlp', MLPClassifier(max_iter=10000))])
        pipe_rfc = Pipeline([('rfc', RandomForestClassifier())])
    
    predictors = {"svm":[par_svm, pipe_svm], "knn":[par_knn, pipe_knn], "dcc":[par_dcc, pipe_dcc], "mlp":[par_mlp, pipe_mlp], "rfc":[par_rfc, pipe_rfc]}
    
    for pred in predictors: #iterating over predictors
        grid = GridSearchCV(predictors[pred][1], param_grid=predictors[pred][0], cv=5, scoring = 'balanced_accuracy')  #entering the predictor, and parameters
        grid.fit(X_train, y_train)
        print(label, "score = %3.2f" %(grid.score(X_test,y_test)), str(grid.best_params_))
        save.append('\t'.join([label, "score = %3.2f" %(grid.score(X_test,y_test)), str(grid.best_params_)])+'\n')
        
v = open('gridResults_%s.txt' % protData,'w')
v.writelines(save)
v.close()