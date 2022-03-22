from sgdlog folder: results all seem bad regardless of whether gridsearch is used

from sgdsvm folder: results seem slightly better when i used balanced class weights
(between no balancing and with balancing). results also seem slightly better when precision
rather than accuracy is used for grid search (using balanced class weights)

from svm folder: results seem better compared to using sgd. Grid search indicates that
it prefers no balancing of class weights compared to balancing, but results indicate
balancing is better. Probably because grid search doesn't focus more on SM which is what I want.
Need to be careful with grid search, use personal judgment to preselect some hyperparameters,
and let grid search optimise only a selected few.

from rf folder: results seem around or slightly worse than svm. Grid search indicates that best
max_features is 3 when this hyperparameter is allowed to vary.

from rf_os folder: oversampling may help a bit, but max_features could be around 3, as grid
searching around a wide range of this number yields a slightly worse result.

combining_data.py
- script to combine all my features and labels
data_preprocessing.py
- data preprocessing script to take output of combining_data.py, and prepare it
for ML work

adding_PNAS_labels.py
- using PNAS labels from the output of combining_data.py

from pnas_labels folder: Am doing the PNAS paper method, get better result, but still different from
them. Noticed that even after 100 runs, the scores don't vary that much.