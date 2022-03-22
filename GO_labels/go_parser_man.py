# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:25:38 2020

@author: weixiong001
Doesn't work. Has bugs so ignore.
"""

import csv

master_dict = {}

with open('go.obo', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if len(row) == 0:
            continue
        if 'obsolete' in row[0]:
            continue
        
        if row[0].startswith('id:'):
            value = row[0].split(' ')[1]
        if row[0].startswith('is_a'):
            key = row[0].split(' ')[1]
            if key not in master_dict:
                master_dict[key] = [value]
            else:
                master_dict[key].append(value)
            
key = 'GO:0007005'
# 26 child terms + itself = 7
# ['GO:0000002', 'GO:0000266', 'GO:0007006', 'GO:0007287', 'GO:0008053', 
#  'GO:0008637', 'GO:0030382', 'GO:0048311', 'GO:0061726', 'GO:0070584', 
#  'GO:0097250', 'GO:0033955', 'GO:0007007', 'GO:0007008', 'GO:0046902', 
#  'GO:0051204', 'GO:0090151', 'GO:1990613', 'GO:1990046', 'GO:0001836', 
#  'GO:0032976', 'GO:0043653', 'GO:1902108', 'GO:0000001', 'GO:0048312', 
#  'GO:0000422']

ans = []

def recur_get(master_d, k):
    temp = master_d[k]
    for i in temp:
        if i not in master_d:
            return []
        else:
            return temp + recur_get(master_d, i)
if key in master_dict:
    pass
            
 
            