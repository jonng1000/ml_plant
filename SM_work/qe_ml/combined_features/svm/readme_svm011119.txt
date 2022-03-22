SVM scripts

svm.py -> first script ran, produced the following outputs:
	- svm_lc.png
	- svm_roc.png
Used grid search on these hyperparameters:
grid_param = {
        'kernel': ['linear', 'rbf'],
        'C': [0.001, 0.01, 0.1, 1, 10],
        'gamma': [0.001, 0.01, 0.1, 1],
}
Grid search is used to maximise precision, class weights not balanced.
Results are meh, SM precision is 0.33 and recall is 0.05.

svm_cwb.py -> second script ran, produced the following outputs:
	- svm_lc_cwb.png
	- svm_cwb_roc.png
Used grid search on these hyperparameters:
grid_param = {
        'kernel': ['linear', 'rbf'],
        'C': [0.001, 0.01, 0.1, 1, 10],
        'gamma': [0.001, 0.01, 0.1, 1],
}
Grid search is used to maximise precision, class weights balanced.
Results are meh, SM precision is 0.14 and recall is 0.24. Maybe better than not balancing class
weights?

swm_cwb_Cgamma.py -> third script ran, produced the following outputs:
	- svm_Cgamma_roc.png
Used grid search on these hyperparameters:
grid_param = {
        'kernel': ['linear', 'rbf'],
        'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        'gamma': [0.001, 0.01, 0.1, 1, 10, 100]
}
Grid search is used to maximise precision, class weights balanced. More hyperparameters for
grid search compared to earlier two scripts.
Results seem similar to svm.py, SM precision is 0.33 and recall is 0.07.
Maybe slightly worse that swm_cwb.py? 
Maybe testing over a larger range is not so good? Could be due to the same reason why grid search
says no balanncing of class weights is better.
Grid search selected large gamma, which means a complicated function could be used for fittin

swm_gscw.py -> fourth script ran, produced the following outputs:
	- svm_lc_gscw.png
	- svm_roc_gscw.png
Used grid search on these hyperparameters:
grid_param = {
        'kernel': ['linear', 'rbf'],
        'C': [0.001, 0.01, 0.1, 1, 10],
        'gamma': [0.001, 0.01, 0.1, 1],
        'class_weight': [None, 'balanced']
}
Grid search is used to maximise precision, class weights used in grid search.
Similar range of hyperparameters compared to svm_cwb.py 
Grid search indicates that no balancing of class weights is better.
Results seem similar to svm.py, SM precision is 0.33 and recall is 0.04.
Maybe slightly worse that swm_cwb.py?
(wrt readme_sgdsvm_311019.txt) Why grid search says no balanncing of class weights is better?
This doesn't seem to make sense and probably is because grid search looks at overal score,
whereas I focus more on SM. Can use the output of this script as evidence

