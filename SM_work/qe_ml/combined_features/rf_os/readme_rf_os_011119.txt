RF OS scripts - RF scripts with oversampling

rf_manyp_os.py -> first script ran, produced the following outputs:
	- rf_os_lc.png
	- rf_os_auc.png
Used grid search on these hyperparameters:
grid_param = {
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
    'max_features': [1, 2, 3, 4, 5],
    'bootstrap': [True, False]
}
Grid search is used to maximise precision, class weights balanced.
Results are meh, SM precision is 0.60 and recall is 0.11.
Grid search indicates that best max_features is 1. Not sure if only 1 feature 
used for splitting is good? Previous RF run (rf_cwb_boot_mp.py) indicate that max_features is 3, 
which would be around the default value for my data.

rf_f34_os.py -> second script ran, produced the following outputs:
	- rf_f34os_lc.png
	- rf_f34os_auc.png
Used grid search on these hyperparameters:
grid_param = {
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
    'max_features': [3, 4],
    'bootstrap': [True, False]
}
Grid search is used to maximise precision, class weights balanced.
Results are slight better compared to above, SM precision is 0.59 and recall is 0.19.
Restricted number of features for grid search to 3 and 4, as I'm not sure if using only 1 feature 
used for splitting is good? rf_manyp_os.py selected 1 feature, but this may be wrong. max_features of 3, 
would be around the default value for my data.

Conclusion from above two scripts:
Oversampling may help a bit, but max_features could be around 3, as grid
searching around a wide range of this number yields a slightly worse result.

