# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:46:11 2020

@author: weixiong001

Test subprocess
"""

import pandas as pd
import pickle
import sys

# Doesn't work
#number = sys.argv[1]
#data = pickle.loads(sys.stdin.buffer.read())
#data = data.iloc[0:20, 0:20]
#sys.stdout.buffer.write(pickle.dumps(data))

# Works
data = pickle.loads(sys.stdin.buffer.read())
data = data.iloc[0:20, 0:20]
sys.stdout.buffer.write(pickle.dumps(data))

