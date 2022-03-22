# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:52:15 2021

@author: weixiong001

Checks log file (summarised version) to make sure there's no unexpected error
messages, prints them out if there is.

Error messages which I am looking at are errors related to too much memory used
"""
import csv


FILE = 'log_110621_summary_blanks.txt'

with open(FILE, newline='') as csvfile:
    file_reader = csv.reader(csvfile, delimiter='\t')
    for row in file_reader:
        if len(row) == 0:
            continue
        if row[0].startswith('Script'):
            continue
        if row[0].startswith('go_GO'):
            continue
        # If there's any weird error messages, will be showed here
        print(row)

