# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:05:33 2020

@author: weixiong001

Takes in Marek's ouput from his PCC script, and reformats it, so that each
line only has one gene pair with its associated PCC value, each string in each
line is separated with a tab space.

Takes about 6min to run
"""

import csv
import re

FILE = 'ARATH.PCC.txt'
OUTPUT = 'Ath_proc.PCC.txt'

mega_lst = []
with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for row in csvreader:
        a_row_ml = []
        gene_A = row[0].split(':')[0]
        gene_B = row[0].split(' ')[1].split('(')[0]
        pcc = re.search('\(([^)]+)', row[0].split(' ')[1]).group(1)
        a_row_ml.append(gene_A)
        a_row_ml.append(gene_B)
        a_row_ml.append(pcc)
        mega_lst.append(a_row_ml)
        
        if len(row) > 1:
            for i in range(1, len(row)):
                a_row_ml = []
                gene_next = row[i].split('(')[0]
                pcc_next = re.search('\(([^)]+)', row[i]).group(1)
                a_row_ml.append(gene_A)
                a_row_ml.append(gene_next)
                a_row_ml.append(pcc_next)
                mega_lst.append(a_row_ml)                


with open(OUTPUT, 'w', newline='') as csvfile2:
    csvwriter = csv.writer(csvfile2, delimiter='\t')
    for write_row in mega_lst:
        csvwriter.writerow(write_row)