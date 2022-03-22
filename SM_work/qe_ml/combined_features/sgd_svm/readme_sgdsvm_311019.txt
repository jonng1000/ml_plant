Stochastic Gradient Descent (SGD) scripts - SVM

sgdsvm.py -> first script ran, produced the following outputs:
	- sgdsvm.png
Used grid search on these hyperparameters:
grid_param = {
    'penalty': ['l2', 'l1', 'elasticnet'],
    'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive']
}
Grid search is used to maximise precision.
Used eta0=.01: not useful as v bad classification results,
doesnt identify SM at all.

sgdsvm_cwb.py -> first script ran, produced the following outputs:
	- sgdsvm_cwb_lc.png
	- sgdsvm_cwb_roc.png
Used grid search on these hyperparameters:
grid_param = {
    'penalty': ['l2', 'l1', 'elasticnet'],
    'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive']
}
Grid search is used to maximise precision.
Used eta0=.01 and balanced class weights: slighty better results,
SM precision is 0.11 and recall is 0.79, but not very good. 
Balanced class weights seem to be better.
Note: Here, I also included class weights = ['balanced', none] as a hyperparameter for gridsearch
but it said none is better. This doesn't seem to make sense and probably is because grid search
looks at overal score, whereas I focus more on SM. Didn't save results for this tho.

sgdsvm_cwb_acc.py -> third script ran, produced the following outputs:
	- sgdsvm_cwb_acc_roc.png
Used grid search on these hyperparameters:
grid_param = {
    'penalty': ['l2', 'l1', 'elasticnet'],
    'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive']
}
Grid search is used to maximise accuracy.
Used eta0=.01: slighty worse results compared to sgdsvm_cwb.py, SM precision is 0.10 and recall is 0.68.
Probably precision is a better measure since accuracy is less important for me due to unbalanced class
sets (wrt readme_sgdlog_31019.txt).


