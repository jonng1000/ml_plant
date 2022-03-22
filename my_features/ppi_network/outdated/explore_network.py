# -*- coding: utf-8 -*-
"""
Created on 230620

@author: weixiong
Explores the Biogrid PPI network for all species
"""

import pandas as pd

# Loading complete biogrid database, all species
FILE = 'BIOGRID-ALL-4.0.189.tab3.txt'

df = pd.read_csv(FILE, sep='\t')

m1 = df['Organism Name Interactor A'].str.contains('Arabidopsis', regex=False)
m2 = df['Organism Name Interactor B'].str.contains('Arabidopsis', regex=False)
'''
>>> df.loc[:,'Experimental System Type']
0          physical
1          physical
2          physical
3          physical
4          physical
             ...
1868156    physical
1868157    physical
1868158    physical
1868159    physical
1868160    physical
Name: Experimental System Type, Length: 1868161, dtype: object
>>> df.loc[:,'Experimental System Type'].unique()
array(['physical', 'genetic'], dtype=object)
'''
'''
>>> df.loc[df['Organism Name Interactor A'].str.contains('Arabidopsis', regex=False),:]
         #BioGRID Interaction ID  ...       Organism Name Interactor B
126011                    251838  ...  Arabidopsis thaliana (Columbia)
126012                    251839  ...  Arabidopsis thaliana (Columbia)
136834                    265014  ...  Arabidopsis thaliana (Columbia)
136835                    265015  ...  Arabidopsis thaliana (Columbia)
136836                    265016  ...  Arabidopsis thaliana (Columbia)
...                          ...  ...                              ...
1863084                  2771530  ...  Arabidopsis thaliana (Columbia)
1863085                  2771531  ...  Arabidopsis thaliana (Columbia)
1863086                  2771532  ...  Arabidopsis thaliana (Columbia)
1863087                  2771533  ...  Arabidopsis thaliana (Columbia)
1863088                  2771534  ...  Arabidopsis thaliana (Columbia)

[58575 rows x 37 columns]
>>> df.loc[m1 & m2, :]
         #BioGRID Interaction ID  ...       Organism Name Interactor B
126011                    251838  ...  Arabidopsis thaliana (Columbia)
126012                    251839  ...  Arabidopsis thaliana (Columbia)
136834                    265014  ...  Arabidopsis thaliana (Columbia)
136835                    265015  ...  Arabidopsis thaliana (Columbia)
136836                    265016  ...  Arabidopsis thaliana (Columbia)
...                          ...  ...                              ...
1863084                  2771530  ...  Arabidopsis thaliana (Columbia)
1863085                  2771531  ...  Arabidopsis thaliana (Columbia)
1863086                  2771532  ...  Arabidopsis thaliana (Columbia)
1863087                  2771533  ...  Arabidopsis thaliana (Columbia)
1863088                  2771534  ...  Arabidopsis thaliana (Columbia)

[58391 rows x 37 columns]
'''
ath_only = df.loc[m1 & m2, :]

# Loading complete biogrid database, all species
FILE2 = 'BIOGRID-ORGANISM-Arabidopsis_thaliana_Columbia-4.0.189.tab3.txt'

df2 = pd.read_csv(FILE2, sep='\t')
'''
>>> df2
       #BioGRID Interaction ID  ...       Organism Name Interactor B
0                       251838  ...  Arabidopsis thaliana (Columbia)
1                       251839  ...  Arabidopsis thaliana (Columbia)
2                       265014  ...  Arabidopsis thaliana (Columbia)
3                       265015  ...  Arabidopsis thaliana (Columbia)
4                       265016  ...  Arabidopsis thaliana (Columbia)
...                        ...  ...                              ...
58770                  2771530  ...  Arabidopsis thaliana (Columbia)
58771                  2771531  ...  Arabidopsis thaliana (Columbia)
58772                  2771532  ...  Arabidopsis thaliana (Columbia)
58773                  2771533  ...  Arabidopsis thaliana (Columbia)
58774                  2771534  ...  Arabidopsis thaliana (Columbia)

[58775 rows x 37 columns]
'''
#ydropped_df.to_csv(OUTPUT, sep='\t')

