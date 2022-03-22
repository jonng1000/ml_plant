# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:43:18 2021

@author: weixiong001

Takes in output from IPC, and produces a dataframe from it
"""

import pandas as pd
import csv

FILE= 'results_JN.csv'
OUTPUT = 'processed_results.txt'

lst_of_lsts = []
with open(FILE, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    first = next(reader)
    temp = first[0][1:]
    first[0] = temp
    my_header = ['Gene', 'mw']
    my_header.extend(first)
    lst_of_lsts.append(my_header)
    next(reader)  # Second row is empty
    count = 0
    for row in reader:
        if row[0][0] == '>':
            one_row = []
            gene_id = row[0].split('||')[0][1:]
            mw = row[0].split('weight: ')[1].split(' ')[0]
            one_row.append(gene_id)
            one_row.append(mw)
            count += 1       
        elif count == 1:
            one_row.extend(row)
            lst_of_lsts.append(one_row)
            count +=1
        elif count == 2:
            count = 0

prot_info = pd.DataFrame.from_records(lst_of_lsts[1:], columns=lst_of_lsts[0])
df = prot_info.set_index('Gene')
df = df.astype('float64')
'''
# My fasta file has 27654 genes, the below is correct, since the one
# extra item is due to my header file
len(lst_of_lsts)
Out[132]: 27655
'''
df.to_csv(OUTPUT, sep='\t')

#Only has about 14k genes in the AT*G/M/C format so shall not use this, use
# Used the author's calculator 2.0 to calculate for mine