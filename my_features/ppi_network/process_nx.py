# -*y- coding: utf-8 -*-
"""
Created on 011020

@author: weixiong

Plots degree distribution from Arabidopsis ppi, and saves it to a picture
"""
import collections
import networkx as nx
import matplotlib.pyplot as plt

FILE = 'ath_ppi.graphml'
PICTURE = 'deg_dist'

G = nx.read_graphml(FILE)
'''
>>> G.number_of_nodes()
10585
>>> G.number_of_edges()
50429
'''
degree_sequence = sorted([d for n, d in G.degree()])
degree_count = collections.Counter(degree_sequence)
deg, cnt = zip(*degree_count.items())

fig, ax = plt.subplots()
ax.scatter(deg, cnt, s=20)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Degree distribution")
ax.set_ylabel("Count (log10)")
ax.set_xlabel("Degree (log10)")

fig.savefig(PICTURE + ".png")
