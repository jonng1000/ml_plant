Stochastic Gradient Descent (SGD) scripts - logistic regression
- for grid search, need to set eta0 > 0, otherwise it can't run, so set it at eta0 = 0.1

training_ML_sgdlog.py -> first script ran for building ML modes, produced some test plots:
	- scree_test_311019.png
	- pca_test_311019.png
	- heatmap_corr.png
	these plots are just to explore the data, but probably not that essential so can skip
	in future
	Produced the following outputs:
	- log_default_311019.png
	- log_default_roc_311019.png
Used eta0=.01: not useful as v bad classification results,
doesnt identify SM at all. Didn't use gridsearch and data is unbalanced.

training_ML_sgdlog_grid.py -> second script ran. Produced the following outputs:
	- log_gs_roc_311019.png
Used grid search on these hyperparameters:
grid_param = {
    'penalty': ['l2', 'l1', 'elasticnet'],
    'fit_intercept': [True, False],
    'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive']
}
Grid search is used to maximise accuracy.
Used eta0=.01, but same results as without grid search,
bad resuls as SM genes are not identified.

training_ML_sgdlog_grid_veta.py -> third script ran. Produced the following outputs:
	- log_gs_veta_roc_311019.png
Used grid search on these hyperparameters:
grid_param = {
    'penalty': ['l2', 'l1', 'elasticnet'],
    'fit_intercept': [True, False],
    'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive'],
    'eta0': [0.01, 0.03, 0.05, 0.07]
}
Grid search is used to maximise precision. I think precision could be better as I want to
focus on precise identification of SM genes. 
Same results as without grid search,
bad resuls as SM genes are not identified.

Output when running my script from command line:

(base) workstation@Workstation-MutwilLab:~/JN/machine_learning/models$ python rf_manyp_os.py
{'bootstrap': False, 'criterion': 'gini', 'max_features': 2, 'n_estimators': 100}
0.9873160709743908
[learning_curve] Training set sizes: [ 193  386  579  772  966 1159 1352 1545 1738 1932]
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 12 concurrent workers.
[Parallel(n_jobs=-1)]: Done 100 out of 100 | elapsed:    2.1s finished
              precision    recall  f1-score   support

           0       0.95      0.98      0.96       289
           1       0.36      0.20      0.26        20

    accuracy                           0.93       309
   macro avg       0.65      0.59      0.61       309
weighted avg       0.91      0.93      0.92       309

(base) workstation@Workstation-MutwilLab:~/JN/machine_learning/models$ python rf_manyp_os.py
{'bootstrap': False, 'criterion': 'gini', 'max_features': 3, 'n_estimators': 100}
0.9882949538951976
[learning_curve] Training set sizes: [ 194  388  582  777  971 1165 1360 1554 1748 1943]
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 12 concurrent workers.
[Parallel(n_jobs=-1)]: Done 100 out of 100 | elapsed:    2.0s finished
              precision    recall  f1-score   support

           0       0.90      0.99      0.94       277
           1       0.43      0.09      0.15        32

    accuracy                           0.89       309
   macro avg       0.67      0.54      0.55       309
weighted avg       0.85      0.89      0.86       309

-> Can run these on command line, just need to insert line breaks and names for the info that I'm
getting on the screen