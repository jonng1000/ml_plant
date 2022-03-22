# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 19:28:47 2022

@author: weixiong001

Converts final processed file into json, and ensures format is compatible
with Swee Kwang's overallData.json format
"""

import pandas as pd
import json

FILE = 'processed_stage4.txt'
OUTPUT = 'overallData.json'

df = pd.read_csv(FILE, index_col=0 , sep='\t')
df = df.rename(columns={'Category': 'category', 'Feature name': 'feature',
                        'Description':'description'})
df['id'] = '-'
result = df.to_json(orient="records")
parsed = json.loads(result)
json_object = json.dumps(parsed, indent=4) 

# Writing to sample.json
with open(OUTPUT, 'w') as outfile:
    outfile.write(json_object)

