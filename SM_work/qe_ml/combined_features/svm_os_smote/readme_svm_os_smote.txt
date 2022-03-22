svm_os.py script
- svm with oversampling to 1000 SM genes
- meh results, same as svm without oversampling

svm_os_bw.py script 
- oversample SM to 300 only, and use balanced class weights - better results

              precision    recall  f1-score   support

           0       0.95      0.89      0.92       287
           1       0.22      0.41      0.29        22

    accuracy                           0.85       309
   macro avg       0.59      0.65      0.60       309
weighted avg       0.90      0.85      0.87       309

- mathematically, oversampling and balanced class weights is supposed to be equivalent, so not
sure why this works

swm_smote.py script
- oversampling using SMOTE, create artificial data
results:

best_parameters
{'C': 10, 'gamma': 1, 'kernel': 'rbf'}
Fitting model and printing classification report
              precision    recall  f1-score   support

           0       0.95      0.78      0.86       288
           1       0.13      0.43      0.20        21

    accuracy                           0.76       309
   macro avg       0.54      0.61      0.53       309
weighted avg       0.89      0.76      0.81       309

precision: TP/(TP+FP) -> out of all your selected SM genes,
how many are actually SM genes?
recall: TP/(TP+FN) -> out of all the total number of actual SM genes,
how many SM genes did I select?

- meh results

svm_smote_enc.py script
- used a SMOTE variant which is designed to handle continuous and categorical data

results:

Finished data preprocessing
best_parameters
{'C': 1, 'gamma': 1, 'kernel': 'rbf'}

Creating learning curve
[learning_curve] Training set sizes: [ 207  414  621  828 1035 1242 1449 1656 1863 2070]
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 4 concurrent workers.
[Parallel(n_jobs=-1)]: Done 100 out of 100 | elapsed:    7.0s finished

Fitting model and printing classification report
              precision    recall  f1-score   support

           0       0.96      0.75      0.84       286
           1       0.16      0.61      0.26        23

    accuracy                           0.74       309
   macro avg       0.56      0.68      0.55       309
weighted avg       0.90      0.74      0.80       309

precision: TP/(TP+FP) -> out of all your selected SM genes,
how many are actually SM genes?
recall: TP/(TP+FN) -> out of all the total number of actual SM genes,
how many SM genes did I select?

Creating auc plot

- gives slightly better results than regular SMOTE