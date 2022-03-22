Scripts
build_RF_score.py -> Builds features block by block, with a RF model.
build_RF_score_ran.py -> Builds features block by block, with a RF model
and randomises it
build_RF_score_v2.py -> Improved version of build_RF_score,  produces:
    - rfm_scores_100.txt
    - rfm_scores_1000.txt
    - rfm_scores_9000.txt
    - rfm_scores_9537.txt
Includes both original and randomly shuffled features.
Time taken for script to run:
- top 10 - 100 features: 5min to run (earlier version of script)
- top 100 - 1000 features: 10min to run
- top 1000 - 9000 features: 40min to run
total time: ~1h
explore.py -> plots scores from build_RF_score_ran.py and build_RF_score.py
explore_building.py -> plots scores from build_RF_score_v2.py. Remove duplicate runs
from output of that script
rfe_module.py -> based on rf_feature_extract.py, for importing functions to build RF model
rfe_module_v2.py -> improved version of rfe_module.py

Output
rfm_feat.txt -> feature importance after 100 runs
rfm_scores.txt -> RF scores, building features 0-100, blocks of 10, features
not randomised
rfm_scores_ran.txt -> same as rfm_scores.txt, but with randomised features
rfm_scores_100.txt
rfm_scores_1000.txt
rfm_scores_9000.txt
rfm_scores_9537.txt
-> Above 4 files are the important ones, build RF models from 0-100 with blocks of 10,
100-1000 with blocks of 100, 1000-9000 with blocks of 1000, last one with 9537 features.
Has original features and randomised ones. Used this to produce plots showing model
scores with the addition of more features

Plots
scores_build_all.png
scores_build_100.png
scores_build_200.png
scores_build_1000.png
-> Above 4 plots are from explore_building.py, see model score where all features are in, and
100, 200 and 1000 features are in 
scores_building.png -> earlier version of plot, can ignore