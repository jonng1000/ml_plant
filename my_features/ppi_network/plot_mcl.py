# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Plots mcl gene cluster distribution, and saves it to a picture
"""
import collections
import pandas as pd
import matplotlib.pyplot as plt

FILE = 'ath_ppi_clusters.txt'
# If plotting histogram, uncomment this, comment out scatterplot code
PICTURE = 'clusters_hist2.png'
#PICTURE = 'clusters_dist.png'

df = pd.read_csv(FILE, index_col=0,  sep='\t')
sizes = df.drop_duplicates()['cluster_size']

size_count = collections.Counter(sizes.sort_values(ascending=False))
s, cnt = zip(*size_count.items())

fig, ax = plt.subplots()
# If plotting histogram, uncomment this, comment out scatterplot code
# Can try with default bin size but it doesn't look nice
ax.hist(sizes, bins=100)
#ax.scatter(s, cnt, s=20)
# If plotting histogram, comment out this
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Cluster distribution")
# If plotting histogram, uncomment this, comment out scatterplot code 
#ax.set_ylabel("Cluster Count")
#ax.set_xlabel("Cluster size")
ax.set_ylabel("Clsuter Count (log10)")
ax.set_xlabel("Cluster size (log10)")
fig.savefig(PICTURE)
