"""
Calculates mutual information (mi)

Note: Running the mi function on a large dataset takes 5min, but running it
repeated on several large datasets also takes 5min
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif

#################################################################################
# Basic tests of how the mi function works
#################################################################################
"""
>>> test1 = np.array([1, 1, 0, 0])
>>> test2 = np.array([0, 0, 1, 0])
>>> mutual_info_classif(test1.reshape(-1,1), test2)
array([5.55111512e-17])
>>> mutual_info_classif(test2.reshape(-1,1), test1)
array([0.20833333])
# mi is supposed to be symmetrical
# but i get diff ans above, coz I need to set the
# discrete_features parameter correctly, otherwise
# sklearn guess whether the feature is continuous/discrete
# and it may guess wrong.
>>> test3 = np.random.randint(0,2,100)
>>> test4 = np.random.randint(0,2,100)
>>> mutual_info_classif(test3.reshape(-1,1), test4)
array([0.05192125])
>>> mutual_info_classif(test4.reshape(-1,1), test3)
array([0])
>>> mutual_info_classif(test4.reshape(-1,1), test3, discrete_features=True)
array([0.00181933])
>>> mutual_info_classif(test3.reshape(-1,1), test4, discrete_features=True)
array([0.00181933])

>>> from sklearn.feature_selection import mutual_info_regression
>>> test5 = np.random.normal(0, 1, 100)
>>> test6 = np.random.normal(0, 1, 100)
>>> mutual_info_regression(test5.reshape(-1, 1), test6)
array([0.0268278])
>>> mutual_info_regression(test6.reshape(-1, 1), test5)
array([0.0268278])
>>> mutual_info_regression(test5.reshape(-1, 1), test6, discrete_features=False)
array([0.0268278])
>>> mutual_info_regression(test6.reshape(-1, 1), test5, discrete_features=False)
array([0.0268278])
# For these arrays, sklearn manages to guess the nature of the feature
# correctly. If i set discrete_features_True, I get an error here
"""

#################################################################################
# Calculating mi from my golgi dataset
#################################################################################
FILE = 'Golgi_apparatus_GO.txt'
MI_FILE = 'mi_golgi.txt'
CLASS_LABELS = 'AraCyc annotation'
df = pd.read_csv(FILE, sep="\t", index_col=0)

pos = df[CLASS_LABELS].value_counts().idxmin()
neg = df[CLASS_LABELS].value_counts().idxmax()
df.loc[:, 'AraCyc annotation'].replace([pos, neg], [1, 0], inplace=True)
y = df['AraCyc annotation']

default_mi_array = mutual_info_classif(df,y)
default_mi = pd.Series(default_mi_array, index = df.columns)

df_floats = df.select_dtypes(include=['float64'])
df_ints = df.select_dtypes(include=['int64'])
orig_floats_mi_array = mutual_info_classif(df_floats, y, discrete_features=False)
orig_ints_mi_array = mutual_info_classif(df_ints, y, discrete_features=True)
orig_floats_mi = pd.Series(orig_floats_mi_array, index=df_floats.columns)
orig_int_mi = pd.Series(orig_ints_mi_array, index=df_ints.columns)
orig_dtypes_mi = orig_floats_mi.append(orig_int_mi)

"""
# Exploring the nature of my features (discrete or continuous) since that
# affects mi calculations. float64 are continuous and int64 are categorical
>>> df.dtypes.value_counts() 

int64      8887 

float64      60 

dtype: int64 

>>> df.select_dtypes(include=['float64']).columns 

Index(['Functional likelihood', 'Gene family size', 

       'nucleotide diversity (pi)', 'Max percent identity to paralogs', 

       'FayWuH', 'MK-G', 'dS to paralog', 'Retention_rate', 

       'Co-localized SM gene clusters (5 genes)', 

       'Co-localized SM gene clusters (10 genes)', 

       'Co-localized PM gene clusters (5 genes)', 

       'Co-localized PM gene clusters (10 genes)', 

       'Expression Median (development)', 'Expression Max (development)', 

       'Expression Variation (development)', 

       'Expression Breadth (development)', 'abiotic-shoot up-regulation', 

       'abiotic-shoot down-regulation', 'abiotic-shoot up/down regulation', 

       'abiotic-root up-regulation', 'abiotic-root down-regulation', 

       'abiotic-root up/down regulation', 'biotic up-regulation', 

       'biotic down-regulation', 'biotic up/down regulation', 

       'hormone up-regulation', 'hormone down-regulation', 

       'hormone up/down regulation', 'H3K4me3', 'H3K9me1', 'H3K23ac', 'H3K9ac', 

       'H3K9me2', 'H3K4me1', 'H3K27me3', 'H3T3ph', 

       'Co-expressed cluster at k=2000, develop', 'maxPCC to paralog- abiotic', 

       'maxPCC to paralog-biotic', 'maxPCC to paralog-develop', 

       'maxPCC to paralog-hormone', 'max PCC to GM-abiotic', 

       'max PCC to SM-abiotic', 'max PCC to GM-biotic', 'max PCC to SM-biotic', 

       'max PCC to GM-develop', 'max PCC to SM-develop', 

       'max PCC to GM-hormone', 'max PCC to SM-hormone', 'Number of domains', 

       'Amino acid length', 'Protein-protein interactions', 

       'Aranet gene-interactions', 'within_atha_ dNdS', 'alyr_ dNdS', 

       'vvin_ dNdS', 'ptri_ dNdS', 'slyc_ dNdS', 'osat_ dNdS', 'ppat_ dNdS'], 

      dtype='object') 

# Looking at features to identify discrete one, most of the below are discrete
# but some continuous ones are shown here, just to see how they look
>>> df['Functional likelihood'] 

Gene 

AT1G01040    0.938 

AT1G01050    0.938 

AT1G01090    1.000 

AT1G01120    0.990 

AT1G01200    0.570 

             ... 

ATMG00070    0.938 

ATMG00510    0.938 

ATMG00516    0.938 

ATMG01080    0.938 

ATMG01120    0.938 

Name: Functional likelihood, Length: 2586, dtype: float64 

>>> df['Gene family size'] 

Gene 

AT1G01040     7.0 

AT1G01050     6.0 

AT1G01090     6.0 

AT1G01120    21.0 

AT1G01200    76.0 

             ... 

ATMG00070    10.0 

ATMG00510    10.0 

ATMG00516    10.0 

ATMG01080    10.0 

ATMG01120    10.0 

Name: Gene family size, Length: 2586, dtype: float64 

>>> df['nucleotide diversity (pi)'] 

Gene 

AT1G01040    0.001 

AT1G01050    0.000 

AT1G01090    0.002 

AT1G01120    0.001 

AT1G01200    0.007 

             ... 

ATMG00070    0.002 

ATMG00510    0.002 

ATMG00516    0.002 

ATMG01080    0.002 

ATMG01120    0.002 

Name: nucleotide diversity (pi), Length: 2586, dtype: float64 

>>> df['Max percent identity to paralogs'] 

Gene 

AT1G01040    41.82 

AT1G01050    89.72 

AT1G01090    40.71 

AT1G01120    65.09 

AT1G01200    78.79 

             ... 

ATMG00070    70.00 

ATMG00510    70.00 

ATMG00516    70.00 

ATMG01080    70.00 

ATMG01120    70.00 

Name: Max percent identity to paralogs, Length: 2586, dtype: float64 

>>> df['FayWuH'] 

Gene 

AT1G01040   -3.381 

AT1G01050    0.056 

AT1G01090   -1.953 

AT1G01120   -4.778 

AT1G01200   -1.789 

             ... 

ATMG00070   -3.381 

ATMG00510   -3.381 

ATMG00516   -3.381 

ATMG01080   -3.381 

ATMG01120   -3.381 

Name: FayWuH, Length: 2586, dtype: float64 

>>> df['MK-G'] 

Gene 

AT1G01040    0.253 

AT1G01050    0.253 

AT1G01090    0.150 

AT1G01120    0.843 

AT1G01200    0.175 

             ... 

ATMG00070    0.253 

ATMG00510    0.253 

ATMG00516    0.253 

ATMG01080    0.253 

ATMG01120    0.253 

Name: MK-G, Length: 2586, dtype: float64 

>>> df['dS to paralog'] 

Gene 

AT1G01040    1.030 

AT1G01050    2.374 

AT1G01090    1.030 

AT1G01120    1.030 

AT1G01200    1.030 

             ... 

ATMG00070    1.030 

ATMG00510    1.030 

ATMG00516    1.030 

ATMG01080    1.030 

ATMG01120    1.030 

Name: dS to paralog, Length: 2586, dtype: float64 

>>> df['Retention_rate'] 

Gene 

AT1G01040    1.000 

AT1G01050    1.000 

AT1G01090    1.000 

AT1G01120    1.000 

AT1G01200    1.000 

             ... 

ATMG00070    0.714 

ATMG00510    0.625 

ATMG00516    1.000 

ATMG01080    1.000 

ATMG01120    1.000 

Name: Retention_rate, Length: 2586, dtype: float64 

>>> df['Co-localized SM gene clusters (5 genes)'] 

Gene 

AT1G01040    0.0 

AT1G01050    0.0 

AT1G01090    0.0 

AT1G01120    0.0 

AT1G01200    1.0 

            ... 

ATMG00070    0.0 

ATMG00510    0.0 

ATMG00516    0.0 

ATMG01080    0.0 

ATMG01120    0.0 

  

>>> df['Co-localized SM gene clusters (5 genes)'].value_counts() 

0.0    2229 

1.0     263 

2.0      60 

3.0      21 

4.0       9 

5.0       3 

7.0       1 

Name: Co-localized SM gene clusters (5 genes), dtype: int64 

>>> df['Co-localized SM gene clusters (10 genes)'].value_counts() 

0.0     1961 

1.0      424 

2.0      118 

3.0       44 

4.0       26 

5.0        7 

6.0        4 

7.0        1 

13.0       1 

Name: Co-localized SM gene clusters (10 genes), dtype: int64 

>>> df['Co-localized PM gene clusters (5 genes)'].value_counts() 

0.0    925 

1.0    901 

2.0    501 

3.0    190 

4.0     55 

5.0     10 

6.0      2 

7.0      2 

Name: Co-localized PM gene clusters (5 genes), dtype: int64 

>>> df['Co-localized PM gene clusters (10 genes)'].value_counts() 

1.0     668 

2.0     620 

3.0     454 

0.0     430 

4.0     244 

5.0     114 

6.0      38 

7.0      10 

8.0       5 

9.0       2 

10.0      1 

>>> df['abiotic-shoot up-regulation'].value_counts() 

0.0     1414 

1.0      289 

2.0      189 

3.0      129 

4.0      114 

5.0       67 

6.0       63 

7.0       54 

8.0       45 

11.0      37 

9.0       36 

10.0      28 

12.0      24 

13.0      22 

18.0      14 

14.0      13 

15.0      13 

17.0       8 

20.0       6 

16.0       5 

23.0       4 

19.0       4 

24.0       2 

26.0       2 

22.0       2 

25.0       1 

27.0       1 

Name: abiotic-shoot up-regulation, dtype: int64 

>>> df['abiotic-shoot down-regulation'].value_counts() 

0.0     891 

1.0     536 

2.0     276 

3.0     234 

4.0     187 

5.0     135 

6.0      94 

7.0      57 

8.0      41 

9.0      34 

10.0     28 

11.0     25 

12.0     15 

13.0     11 

14.0      9 

15.0      7 

17.0      2 

16.0      1 

20.0      1 

21.0      1 

18.0      1 

 
# Amino acid length is weird, has decimals. Calculating MI gives big differences in results when discrete_features is set to true or False, so just decide to consider it a discrete feature 

>>> df['Amino acid length'].value_counts() 

437.5     340 

217.0      12 

462.0      12 

216.0      12 

348.0      10 

         ... 

1015.0      1 

944.0       1 

752.0       1 

89.0        1 

1450.0      1 

>>> (df['Amino acid length'] % 1).value_counts() 

0.0    2246 

0.5     340 

>>> df['Amino acid length'].describe() 

count    2586.000000 

mean      482.628770 

std       264.713806 

min        64.000000 

25%       325.000000 

50%       437.500000 

75%       547.750000 

max      2481.000000 

Name: Amino acid length, dtype: float64 

# 'Protein-protein interactions' is not discrete, even though it seems to be, because raw data has decimal values. Calculating MI doesn't give big difference in results regardless of whether discrete_features is set to true or False 
"""

#################################################################################
# Creating list discrete features based on work above, then calculate mi
# through various methods and compare the result
#################################################################################
discrete_var = ['Gene family size', 'Co-localized SM gene clusters (5 genes)', 'Co-localized SM gene clusters (10 genes)', 'Co-localized PM gene clusters (5 genes)', 'Co-localized PM gene clusters (10 genes)', 'abiotic-shoot up-regulation',  'abiotic-shoot down-regulation', 'abiotic-shoot up/down regulation', 'abiotic-root up-regulation', 'abiotic-root down-regulation', 'abiotic-root up/down regulation', 'biotic up-regulation', 'biotic down-regulation', 'biotic up/down regulation', 'hormone up-regulation', 'hormone down-regulation', 'hormone up/down regulation', 'Co-expressed cluster at k=2000, develop', 'Number of domains',  'Amino acid length', 'Aranet gene-interactions']
discrete_var.extend(list(df.select_dtypes(include=['int64']).columns))

man_discrete_df = df.loc[:, discrete_var]
man_cont_df = df.drop(columns=discrete_var)
man_discrete_mi_array =  mutual_info_classif(man_discrete_df, y,
                                             discrete_features=True)
man_cont_mi_array =  mutual_info_classif(man_cont_df, y, discrete_features=False)
man_cont_mi = pd.Series(man_cont_mi_array, index=man_cont_df.columns)
man_discrete_mi = pd.Series(man_discrete_mi_array, index=man_discrete_df.columns)
man_dtypes_mi = man_cont_mi.append(man_discrete_mi)

all_discrete_mi_array = mutual_info_classif(df, y, discrete_features=True)
all_discrete_mi = pd.Series(all_discrete_mi_array, index = df.columns)
all_cont_mi_array = mutual_info_classif(df, y, discrete_features=False)
all_cont_mi = pd.Series(all_cont_mi_array, index = df.columns)

"""
# Key mi variables
default_mi -> mi calculations by giving the mi function the entire
dataframe, and letting it figure out automatically which features are discrete
and continuous
orig_dtypes_mi -> mi calculations by specifiying int64 as discrete and float64 as continous and calling  the mi function accordingly
man_dtypes_mi -> mi calculations by specifiying int64 as discrete, manualy looking through float64 features and specifying some of them as discrete, and leaving the rest as continous. Then call the mi function accordingly
all_discrete_mi -> mi calculations by assuming all features are discrete and  calling  the mi function accordingly
all_cont_mi -> mi calculations by assuming all features are continuous  and  calling the mi function accordingly
"""

"""
>>> default_mi.sort_values(ascending=False)
AraCyc annotation            0.336515
suba_golgi                   0.078862
Gene family size             0.044580
maxPCC to paralog-hormone    0.022986
k50_diurnal_cl_11            0.022154
                               ...
c200_dev_cl_164              0.000000
c200_dev_cl_165              0.000000
c200_dev_cl_166              0.000000
c200_dev_cl_167              0.000000
Functional likelihood        0.000000
Length: 8947, dtype: float64
>>> default_mi.sort_values(ascending=False)[:20]
AraCyc annotation             0.336515
suba_golgi                    0.078862
Gene family size              0.044580
maxPCC to paralog-hormone     0.022986
k50_diurnal_cl_11             0.022154
ESSS                          0.020384
alyr_ dNdS                    0.020292
k200_stress_fc_cl_194         0.019824
c200_diurnal_cl_39            0.019669
c200_diurnal_cl_156           0.019457
h100_diurnal_average_cl_28    0.019418
CKS                           0.018887
max PCC to SM-biotic          0.018822
BACK                          0.018460
ILVD_EDD                      0.018293
k100_stress_fc_cl_11          0.018155
DUF4101                       0.018148
Methyltransf_29               0.018088
slycop_homolog                0.017929
k100_diurnal_cl_29            0.017912
dtype: float64

>>> orig_dtypes_mi.sort_values(ascending=False)
AraCyc annotation                          0.336321
suba_golgi                                 0.073368
Gene family size                           0.041326
max PCC to SM-biotic                       0.020574
suba_plastid                               0.020545
                                             ...
Co-expressed cluster at k=2000, develop    0.000000
Aranet gene-interactions                   0.000000
Protein-protein interactions               0.000000
max PCC to GM-biotic                       0.000000
biotic up-regulation                       0.000000
Length: 8947, dtype: float64
>>> orig_dtypes_mi.sort_values(ascending=False)[:20]
AraCyc annotation                           0.336321
suba_golgi                                  0.073368
Gene family size                            0.041326
max PCC to SM-biotic                        0.020574
suba_plastid                                0.020545
dS to paralog                               0.020432
Expression Variation (development)          0.019156
maxPCC to paralog-hormone                   0.018787
Amino acid length                           0.017417
maxPCC to paralog-biotic                    0.016168
maxPCC to paralog- abiotic                  0.015355
Number of domains                           0.014288
Methyltransf_29                             0.013453
max PCC to GM-develop                       0.012141
Co-localized SM gene clusters (10 genes)    0.011203
within_atha_ dNdS                           0.010578
biotic down-regulation                      0.009543
Glyco_transf_8                              0.009221
alyr_ dNdS                                  0.008525
Retention_rate                              0.007554
dtype: float64

>>> man_dtypes_mi.sort_values(ascending=False)
AraCyc annotation           0.336321
Amino acid length           0.146414
Aranet gene-interactions    0.079776
suba_golgi                  0.073368
Gene family size            0.051788
                              ...
H3K4me1                     0.000000
max PCC to GM-hormone       0.000000
ptri_ dNdS                  0.000000
ppat_ dNdS                  0.000000
Functional likelihood       0.000000
Length: 8947, dtype: float64
>>> man_dtypes_mi.sort_values(ascending=False)[:20]
AraCyc annotation                          0.336321
Amino acid length                          0.146414
Aranet gene-interactions                   0.079776
suba_golgi                                 0.073368
Gene family size                           0.051788
maxPCC to paralog-hormone                  0.022641
max PCC to SM-biotic                       0.020962
maxPCC to paralog- abiotic                 0.020830
suba_plastid                               0.020545
maxPCC to paralog-develop                  0.017599
Expression Variation (development)         0.017297
maxPCC to paralog-biotic                   0.015406
dS to paralog                              0.013524
Methyltransf_29                            0.013453
Co-expressed cluster at k=2000, develop    0.011864
within_atha_ dNdS                          0.010241
max PCC to GM-develop                      0.009412
Glyco_transf_8                             0.009221
biotic down-regulation                     0.009191
H3K23ac                                    0.008252
dtype: float64

>>> all_discrete_mi.sort_values(ascending=False)
AraCyc annotation                     3.363215e-01
Expression Max (development)          2.886508e-01
Expression Variation (development)    2.886508e-01
Expression Median (development)       2.878757e-01
Max percent identity to paralogs      2.328454e-01
                                          ...
UPF0052                               8.743006e-16
ERp29                                 8.743006e-16
TMEM192                               8.743006e-16
UN_NPL4                               8.743006e-16
FG-GAP                                8.743006e-16
Length: 8947, dtype: float64
>>> all_discrete_mi.sort_values(ascending=False)[:20]
AraCyc annotation                     0.336321
Expression Max (development)          0.288651
Expression Variation (development)    0.288651
Expression Median (development)       0.287876
Max percent identity to paralogs      0.232845
FayWuH                                0.211726
dS to paralog                         0.160681
maxPCC to paralog-biotic              0.151053
Amino acid length                     0.146414
maxPCC to paralog-hormone             0.144545
maxPCC to paralog-develop             0.140987
maxPCC to paralog- abiotic            0.140065
MK-G                                  0.115246
max PCC to SM-biotic                  0.100939
max PCC to SM-abiotic                 0.098385
max PCC to SM-develop                 0.086335
max PCC to SM-hormone                 0.084873
within_atha_ dNdS                     0.081251
Aranet gene-interactions              0.079776
max PCC to GM-develop                 0.077465
dtype: float64

>>> all_cont_mi.sort_values(ascending=False)
AraCyc annotation            0.336515
suba_golgi                   0.073351
Gene family size             0.043447
maxPCC to paralog-hormone    0.026282
dS to paralog                0.024374
                               ...
Sod_Fe_N                     0.000000
k100_dev_cl_78               0.000000
c50_diurnal_cl_13            0.000000
SLC35F                       0.000000
Functional likelihood        0.000000
Length: 8947, dtype: float64
>>> all_cont_mi.sort_values(ascending=False)[:20]
AraCyc annotation               0.336515
suba_golgi                      0.073351
Gene family size                0.043447
maxPCC to paralog-hormone       0.026282
dS to paralog                   0.024374
h100_stress_fc_ward_cl_49       0.022607
suba_plastid                    0.021745
h100_stress_fc_average_cl_40    0.020663
max PCC to GM-develop           0.020585
h100_dev_complete_cl_17         0.020184
Gal-bind_lectin                 0.019619
k200_dev_cl_84                  0.019574
Amino acid length               0.019119
Rrp15p                          0.019111
max PCC to SM-biotic            0.018732
h200_stress_fc_ward_cl_13       0.018608
Dna2                            0.018433
c200_dev_cl_74                  0.017720
ABA_GPCR                        0.017428
RNA_pol_Rpb2_5                  0.017244
dtype: float64
"""

# Logically, my manual assignment of discrete and continuous features should
# give the best ans, but it (man_dtypes_mi) only shows the suba_golgi feature
# as 3rd most impt. Note: all ranking of importance ignores the most important
# one, which is the class label itself, since that would give the max score as
# it is compared against itself. However, the mi function's auto method of
# determining the type of feature ( default_mi) seems to give the most logical
# ans, as it identifies suba_golgi as the most impt feature

man_mi_df = man_dtypes_mi.sort_values(ascending=False).to_frame()
man_mi_df.index.name = 'Features'
man_mi_df.rename(columns={0: 'mi'}, inplace=True)
man_mi_df.to_csv(MI_FILE, sep='\t')
