# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:52:15 2021

@author: weixiong001

Checks log file to make sure there's no unexpected error
messages, prints them out if there is.

Similar to parse_log_summary.py in 
D:\GoogleDrive\machine_learning\ml_go_workflow\go_runs\vary_hps
but not the same thing
"""
import csv


FILE = 'log290621_9.txt'

with open(FILE, newline='') as csvfile:
    file_reader = csv.reader(csvfile, delimiter='\t')
    for row in file_reader:
        if row[0].startswith('Script'):
            continue
        if 'tested' in row[0]:
            continue
        # If there's any weird error messages, will be showed here
        print(row)

