# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Explores and processes cleaned arabidopsis ppi from Biogrid. Converts ppi into 
graphml format for downstream analysis, and the abc format for mcl
"""

import pandas as pd
import networkx as nx

FILE = 'ath_ppi.txt'
OUTPUT = 'ath_ppi.graphml'
ABC_OUTPUT = 'ath_ppi.abc'

df = pd.read_csv(FILE, sep='\t')
edge_atr = ['Experimental System', 'Experimental System Type',
            'Author', 'Publication Source', 'Throughput', 'Modification']
G = nx.from_pandas_edgelist(df, 'Systematic Name Interactor A',
                            'Systematic Name Interactor B', edge_atr)
'''
>>> G.number_of_nodes()
10585
>>> G.number_of_edges()
50429
'''
# Saves graph in graphml format for downstream analysis
nx.write_graphml_lxml(G, OUTPUT)
# Converts to abc format for mcl
abc = df.loc[:, ['Systematic Name Interactor A',
                 'Systematic Name Interactor B']]
abc.to_csv(ABC_OUTPUT, header=False, index=False, sep=' ')

# Impotant: The below output is on the Biogrid Arabidopsis data directly,
# before its filtered to ensure theres only Arabidopsis and PPI (physical
# interaction info.
# Hence there may be some difference between the filtered network
# and the original network
'''
>>> df.columns
Index(['#BioGRID Interaction ID', 'Entrez Gene Interactor A',
       'Entrez Gene Interactor B', 'BioGRID ID Interactor A',
       'BioGRID ID Interactor B', 'Systematic Name Interactor A',
       'Systematic Name Interactor B', 'Official Symbol Interactor A',
       'Official Symbol Interactor B', 'Synonyms Interactor A',
       'Synonyms Interactor B', 'Experimental System',
       'Experimental System Type', 'Author', 'Publication Source',
       'Organism ID Interactor A', 'Organism ID Interactor B', 'Throughput',
       'Score', 'Modification', 'Qualifications', 'Tags', 'Source Database',
       'SWISS-PROT Accessions Interactor A', 'TREMBL Accessions Interactor A',
       'REFSEQ Accessions Interactor A', 'SWISS-PROT Accessions Interactor B',
       'TREMBL Accessions Interactor B', 'REFSEQ Accessions Interactor B',
y       'Ontology Term IDs', 'Ontology Term Names', 'Ontology Term Categories',
       'Ontology Term Qualifier IDs', 'Ontology Term Qualifier Names',
       'Ontology Term Types', 'Organism Name Interactor A',
       'Organism Name Interactor B'],
      dtype='object')
>>> df['#BioGRID Interaction ID']
0         251838
1         251839
2         265014
3         265015
4         265016
          ...
58770    2771530
58771    2771531
58772    2771532
58773    2771533
58774    2771534
Name: #BioGRID Interaction ID, Length: 58775, dtype: int64
>>> df['Entrez Gene Interactor A']
0        828230
1        828230
2        836259
3        836259
4        836259
          ...
58770    821259
58771    821259
58772    822566
58773    822566
58774    821259
Name: Entrez Gene Interactor A, Length: 58775, dtype: int64
>>> df['Entrez Gene Interactor B']
0        832208
1        821860
2        818903
3        825075
4        836259
          ...
58770    827369
58771    824168
58772    817586
58773    837934
58774    822566
Name: Entrez Gene Interactor B, Length: 58775, dtype: int64
>>> df['BioGRID ID Interactor A']
0        13519
1        13519
2        21503
3        21503
4        21503
         ...
58770     6592
58771     6592
58772     7895
58773     7895
58774     6592
Name: BioGRID ID Interactor A, Length: 58775, dtype: int64
>>> df['BioGRID ID Interactor B']
0        17483
1         7192
2         4240
3        10390
4        21503
         ...
58770    12662
58771     9486
58772     2935
58773    23174
58774     7895
Name: BioGRID ID Interactor B, Length: 58775, dtype: int64
>>> df['Systematic Name Interactor A']
0        AT4G00020
1        AT4G00020
2        AT5G61380
3        AT5G61380
4        AT5G61380
           ...
58770    AT3G01090
58771    AT3G01090
58772    AT3G29160
58773    AT3G29160
58774    AT3G01090
Name: Systematic Name Interactor A, Length: 58775, dtype: object
>>> df['Systematic Name Interactor B']
0        AT5G20850
1        AT3G22880
2        AT2G43010
3        AT3G59060
4        AT5G61380
           ...
58770    AT4G16670
58771    AT3G50060
58772    AT2G30360
58773    AT1G13740
58774    AT3G29160
Name: Systematic Name Interactor B, Length: 58775, dtype: object
>>> df[ 'Synonyms Interactor A']
0        BRCA2A|BREAST CANCER 2 like 2A|EDA20|EMBRYO SA...
1        BRCA2A|BREAST CANCER 2 like 2A|EDA20|EMBRYO SA...
2        APRR1|AtTOC1|MFB13.13|MFB13_13|PRR1|PSEUDO-RES...
3        APRR1|AtTOC1|MFB13.13|MFB13_13|PRR1|PSEUDO-RES...
4        APRR1|AtTOC1|MFB13.13|MFB13_13|PRR1|PSEUDO-RES...
                               ...
58770    AKIN10|SNF1 kinase homolog 10|SNF1-RELATED PRO...
58771    AKIN10|SNF1 kinase homolog 10|SNF1-RELATED PRO...
58772    AKIN11|ATKIN11|SNF1 kinase homolog 11|SNF1-REL...
58773    AKIN11|ATKIN11|SNF1 kinase homolog 11|SNF1-REL...
58774    AKIN10|SNF1 kinase homolog 10|SNF1-RELATED PRO...
Name: Synonyms Interactor A, Length: 58775, dtype: object
>>> df[ 'Synonyms Interactor B']
0        ATRAD51|F22D1.20|F22D1_20|RAS associated with ...
1        ARABIDOPSIS HOMOLOG OF LILY MESSAGES INDUCED A...
2        MFL8.13|MFL8_13|SRL2|phytochrome interacting f...
3        PHYTOCHROME-INTERACTING FACTOR 5|PIF5|phytochr...
4        APRR1|AtTOC1|MFB13.13|MFB13_13|PRR1|PSEUDO-RES...
                               ...
58770                                     DL4360W|FCAALL.2
58771                                myb domain protein 77
58772    CBL-INTERACTING PROTEIN KINASE 11|CIPK11|PKS5|...
58773       ABI five binding protein 2|F21F23.17|F21F23_17
58774    AKIN11|ATKIN11|SNF1 kinase homolog 11|SNF1-REL...
Name: Synonyms Interactor B, Length: 58775, dtype: object
>>> df['Experimental System']
0                 Two-hybrid
1                 Two-hybrid
2                 Two-hybrid
3                 Two-hybrid
4                 Two-hybrid
                ...
58770                    PCA
58771                    PCA
58772                    PCA
58773                    PCA
58774    Synthetic Lethality
Name: Experimental System, Length: 58775, dtype: object
>>> df['Experimental System Type']
0        physical
1        physical
2        physical
3        physical
4        physical
           ...
58770    physical
58771    physical
58772    physical
58773    physical
58774     genetic
Name: Experimental System Type, Length: 58775, dtype: object
>>> df['Author']
0              Siaud N (2004)
1              Siaud N (2004)
2                Ito S (2003)
3                Ito S (2003)
4                Ito S (2003)
                 ...
58770    Carianopol CS (2020)
58771    Carianopol CS (2020)
58772    Carianopol CS (2020)
58773    Carianopol CS (2020)
58774    Carianopol CS (2020)
Name: Author, Length: 58775, dtype: object
>>> df['Publication Source']
0        PUBMED:15014444
1        PUBMED:15014444
2        PUBMED:14634162
3        PUBMED:14634162
4        PUBMED:14634162
              ...
58770    PUBMED:32218501
58771    PUBMED:32218501
58772    PUBMED:32218501
58773    PUBMED:32218501
58774    PUBMED:32218501
Name: Publication Source, Length: 58775, dtype: object
'''
'''
>>> df.columns
Index(['#BioGRID Interaction ID', 'Entrez Gene Interactor A',
       'Entrez Gene Interactor B', 'BioGRID ID Interactor A',
       'BioGRID ID Interactor B', 'Systematic Name Interactor A',
       'Systematic Name Interactor B', 'Official Symbol Interactor A',
       'Official Symbol Interactor B', 'Synonyms Interactor A',
       'Synonyms Interactor B', 'Experimental System',
       'Experimental System Type', 'Author', 'Publication Source',
       'Organism ID Interactor A', 'Organism ID Interactor B', 'Throughput',
       'Score', 'Modification', 'Qualifications', 'Tags', 'Source Database',
       'SWISS-PROT Accessions Interactor A', 'TREMBL Accessions Interactor A',
       'REFSEQ Accessions Interactor A', 'SWISS-PROT Accessions Interactor B',
       'TREMBL Accessions Interactor B', 'REFSEQ Accessions Interactor B',
       'Ontology Term IDs', 'Ontology Term Names', 'Ontology Term Categories',
       'Ontology Term Qualifier IDs', 'Ontology Term Qualifier Names',
       'Ontology Term Types', 'Organism Name Interactor A',
       'Organism Name Interactor B'],
      dtype='object')
>>> df['Organism ID Interactor A']
0        3702
1        3702
2        3702
3        3702
4        3702
         ...
58770    3702
58771    3702
58772    3702
58773    3702
58774    3702
Name: Organism ID Interactor A, Length: 58775, dtype: int64
>>> df['Organism ID Interactor B']
0        3702
1        3702
2        3702
3        3702
4        3702
         ...
58770    3702
58771    3702
58772    3702
58773    3702
58774    3702
Name: Organism ID Interactor B, Length: 58775, dtype: int64
>>> df['Organism ID Interactor A'].unique()
array([  3702, 559292,   9606,   9913,  10116,  10090,  39947,   4577,
        12242, 316407,   9823,   4081,   4098])
>>> df['Organism ID Interactor B'].unique()
array([  3702,   9606, 559292, 284812,  10090,   9913,  39947,   3847,
        12242, 316407,   4577,   3055,  10116,  10298])
>>> df['Organism ID Interactor B'].value_counts()
3702      58591
9606         65
39947        53
559292       34
3847         15
9913          5
284812        3
10090         2
316407        2
10298         1
12242         1
3055          1
4577          1
10116         1
Name: Organism ID Interactor B, dtype: int64
>>> df['Organism ID Interactor A'].value_counts()
3702      58575
9606        129
559292       40
9913          9
10116         6
39947         3
10090         3
4577          3
9823          2
12242         2
4081          1
316407        1
4098          1
Name: Organism ID Interactor A, dtype: int64
>>> df['Throughput']
0        Low Throughput
1        Low Throughput
2        Low Throughput
3        Low Throughput
4        Low Throughput
              ...
58770    Low Throughput
58771    Low Throughput
58772    Low Throughput
58773    Low Throughput
58774    Low Throughput
Name: Throughput, Length: 58775, dtype: object
>>> df['Score']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Score, Length: 58775, dtype: object
>>> df['Score'].unique()
array(['-'], dtype=object)
>>> df['Modification']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Modification, Length: 58775, dtype: object
>>> df['Modification'].unique()
array(['-', 'Phosphorylation', 'Ubiquitination', 'Methylation',
       'Dephosphorylation', 'No Modification', 'Acetylation',
       'Deacetylation', 'Sumoylation', 'Deubiquitination',
       'Proteolytic Processing', 'Desumoylation', 'Prenylation',
       'Ribosylation'], dtype=object)
>>> df['Qualifications']
0           -
1           -
2           -
3           -
4           -
         ...
58770    BiFC
58771    BiFC
58772    BiFC
58773    BiFC
58774       -
Name: Qualifications, Length: 58775, dtype: object
>>> df['Qualifications'].unique()
array(['-',
       'PRR9 expression reducedleaf number reduced, flowering time earlier',
       'leaf number reduced, flowering time earlier',
       'shorter hypocotyl length', 'longer hypocotyl length',
       'cotyledon area reduced in continuous red light',
       'Reduce aprr9 mrna in red light, white light|reduction in APRR9 mRNA in response to light and red light',
# This means I removed some parts here, as the output was too much
...
>>> df['Tags']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Tags, Length: 58775, dtype: object
>>> df['Tags'].unique()
array(['-'], dtype=object)
>>> df['Source Database']
0        BIOGRID
1        BIOGRID
2        BIOGRID
3        BIOGRID
4        BIOGRID
          ...
58770    BIOGRID
58771    BIOGRID
58772    BIOGRID
58773    BIOGRID
58774    BIOGRID
Name: Source Database, Length: 58775, dtype: object
>>> df['Source Database'].unique()
array(['BIOGRID'], dtype=object)
'''
'''
>>> df['SWISS-PROT Accessions Interactor A']
0        Q7Y1C5
1        Q7Y1C5
2        Q9LKL2
3        Q9LKL2
4        Q9LKL2
          ...
58770    Q38997
58771    Q38997
58772    P92958
58773    P92958
58774    Q38997
Name: SWISS-PROT Accessions Interactor A, Length: 58775, dtype: object
>>> df['SWISS-PROT Accessions Interactor B']
0        P94102
1        Q39009
2        Q8W2F3
3        Q84LH8
4        Q9LKL2
          ...
58770         -
58771         -
58772    O22932
58773    Q9LMX5
58774    P92958
Name: SWISS-PROT Accessions Interactor B, Length: 58775, dtype: object
>>> df['TREMBL Accessions Interactor A']
0        F4JGU5
1        F4JGU5
2             -
3             -
4             -
          ...
58770         -
58771         -
58772         -
58773         -
58774         -
Name: TREMBL Accessions Interactor A, Length: 58775, dtype: object
>>> df['TREMBL Accessions Interactor B']
0                    -
1                    -
2        B9DFT8|F4IQ51
3               B9DH29
4                    -
             ...
58770           Q5HZ31
58771           Q9SN12
58772                -
58773                -
58774                -
Name: TREMBL Accessions Interactor B, Length: 58775, dtype: object
>>> df['REFSEQ Accessions Interactor A']
0                  NP_191913|NP_001154192
1                  NP_191913|NP_001154192
2                               NP_200946
3                               NP_200946
4                               NP_200946
                       ...
58770    NP_850488|NP_566130|NP_001118546
58771    NP_850488|NP_566130|NP_001118546
58772       NP_566843|NP_974374|NP_974375
58773       NP_566843|NP_974374|NP_974375
58774    NP_850488|NP_566130|NP_001118546
Name: REFSEQ Accessions Interactor A, Length: 58775, dtype: object
>>> df['REFSEQ Accessions Interactor B']
0                                            NP_568402
1                                            NP_188928
2                                  NP_565991|NP_850381
3        NP_001030890|NP_001030889|NP_851021|NP_191465
4                                            NP_200946
                             ...
58770                                        NP_193400
58771                                        NP_190575
58772                                        NP_180595
58773                                        NP_563933
58774                    NP_566843|NP_974374|NP_974375
Name: REFSEQ Accessions Interactor B, Length: 58775, dtype: object
>>> df['Ontology Term IDs']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term IDs, Length: 58775, dtype: object
>>> df['Ontology Term IDs'].unique()
array(['-', 'APO:0000111', 'APO:0000090', 'APO:0000147|APO:0000087',
       'APO:0000087|APO:0000147', 'APO:0000058', 'APO:0000106',
       'APO:0000106|APO:0000147', 'APO:0000147|APO:0000106'], dtype=object)
>>> df['Ontology Term IDs'].value_counts()
-                          58744
APO:0000111                   22
APO:0000058                    2
APO:0000090                    2
APO:0000106                    1
APO:0000106|APO:0000147        1
APO:0000087|APO:0000147        1
APO:0000147|APO:0000106        1
APO:0000147|APO:0000087        1
Name: Ontology Term IDs, dtype: int64
>>> df['Ontology Term Names']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term Names, Length: 58775, dtype: object
>>> df['Ontology Term Names'].value_counts()
-                                           58744
viability                                      22
metal resistance                                2
peroxisomal morphology                          2
vegetative growth                               1
vegetative growth|heat sensitivity              1
heat sensitivity|resistance to chemicals        1
resistance to chemicals|heat sensitivity        1
heat sensitivity|vegetative growth              1
Name: Ontology Term Names, dtype: int64
>>> df['Ontology Term Categories']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term Categories, Length: 58775, dtype: object
>>> df['Ontology Term Categories'].value_counts()
-                      58744
phenotype                 27
phenotype|phenotype        4
Name: Ontology Term Categories, dtype: int64
>>> df['Ontology Term Qualifier IDs']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term Qualifier IDs, Length: 58775, dtype: object
>>> df['Ontology Term Qualifier IDs'].value_counts()
-      58771
-|-        4
Name: Ontology Term Qualifier IDs, dtype: int64
>>> df['Ontology Term Qualifier Names']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term Qualifier Names, Length: 58775, dtype: object
>>> df['Ontology Term Qualifier Names'].value_counts()
-      58771
-|-        4
Name: Ontology Term Qualifier Names, dtype: int64
>>> df['Ontology Term Types']
0        -
1        -
2        -
3        -
4        -
        ..
58770    -
58771    -
58772    -
58773    -
58774    -
Name: Ontology Term Types, Length: 58775, dtype: object
>>> df['Ontology Term Types'].value_counts()
-                                58746
partial rescue                      15
wild type                            6
partial rescue|partial rescue        4
undetermined                         4
Name: Ontology Term Types, dtype: int64
>>> df[ 'Organism Name Interactor A']
0        Arabidopsis thaliana (Columbia)
1        Arabidopsis thaliana (Columbia)
2        Arabidopsis thaliana (Columbia)
3        Arabidopsis thaliana (Columbia)
4        Arabidopsis thaliana (Columbia)
                      ...
58770    Arabidopsis thaliana (Columbia)
58771    Arabidopsis thaliana (Columbia)
58772    Arabidopsis thaliana (Columbia)
58773    Arabidopsis thaliana (Columbia)
58774    Arabidopsis thaliana (Columbia)
Name: Organism Name Interactor A, Length: 58775, dtype: object
>>> df[ 'Organism Name Interactor B']
0        Arabidopsis thaliana (Columbia)
1        Arabidopsis thaliana (Columbia)
2        Arabidopsis thaliana (Columbia)
3        Arabidopsis thaliana (Columbia)
4        Arabidopsis thaliana (Columbia)
                      ...
58770    Arabidopsis thaliana (Columbia)
58771    Arabidopsis thaliana (Columbia)
58772    Arabidopsis thaliana (Columbia)
58773    Arabidopsis thaliana (Columbia)
58774    Arabidopsis thaliana (Columbia)
Name: Organism Name Interactor B, Length: 58775, dtype: object
>>> df[ 'Organism Name Interactor A'].value_counts()
Arabidopsis thaliana (Columbia)     58575
Homo sapiens                          129
Saccharomyces cerevisiae (S288c)       40
Bos taurus                              9
Rattus norvegicus                       6
Oryza sativa (Japonica)                 3
Mus musculus                            3
Zea mays                                3
Tobacco Mosaic Virus                    2
Sus scrofa                              2
Escherichia coli (K12/W3110)            1
Solanum lycopersicum                    1
Nicotiana tomentosiformis               1
Name: Organism Name Interactor A, dtype: int64
>>> df[ 'Organism Name Interactor B'].value_counts()
Arabidopsis thaliana (Columbia)     58591
Homo sapiens                           65
Oryza sativa (Japonica)                53
Saccharomyces cerevisiae (S288c)       34
Glycine max                            15
Bos taurus                              5
Schizosaccharomyces pombe (972h)        3
Escherichia coli (K12/W3110)            2
Mus musculus                            2
Chlamydomonas reinhardtii               1
Human Herpesvirus 1                     1
Tobacco Mosaic Virus                    1
Zea mays                                1
Rattus norvegicus                       1
Name: Organism Name Interactor B, dtype: int64
'''
