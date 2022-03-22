RF scripts

rf_cwb.py -> first script ran, produced the following outputs:
	- rf_lc_cwb.png
	- rf_cwb.png
Used grid search on these hyperparameters:
grid_param = {
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
    'bootstrap': [True, False]
}
Grid search is used to maximise precision, class weights balanced.
Results are meh, SM precision is 0.50 and recall is 0.12.

rf_cwb_boot.py -> first script ran, produced the following outputs:
	- rf_lc_cwb_boot.png
	- rf_cwb_boot.png
Used grid search on these hyperparameters:
grid_param = {
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy']
}
Grid search is used to maximise precision, class weights balanced.
Bootstrap = True
Results seems worse than rf_cwb.py, SM precision is 1.00 and recall is 0.04. Perhaps
Bootstrap should not be True.

rf_cwb_boot_mp.py -> first script ran, produced the following outputs:
	- rf_lc_cwb_boot_mp.png
	- rf_cwb_boot_mp.png
Used grid search on these hyperparameters:
grid_param = {
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
    'max_features': [1, 2, 3, 4, 5],
    'bootstrap': [True, False]
}
Grid search is used to maximise precision, class weights balanced.
Large range of hyperparameters to be tested. Takes a longer while now to finish grid search.
Grid search indicates that best max_features is 3 when this hyperparameter is allowed to vary.
Results seems slightly better, SM precision is 0.75 and recall is 0.17.





