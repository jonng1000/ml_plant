#!/usr/bin/env python3
#This script calculates the HRR of gene pair PCCs
#Erielle Villanueva - 29 Sep 2020

path = 'D:/GoogleDrive/machine_learning/my_features/coexp_network/' #replace with own path
filename = 'Ath_proc.PCC.txt' #replace with own file

#Function that outputs gene:rank dictionary, takes gene:pcc dictionary as argument
def rank(gene_dict):
  pcc = sorted(gene_dict, key=gene_dict.get, reverse=True) #creates list of genes sorted by PCCs, highest to lowest
  rank_dict = {gene:rank for rank, gene in enumerate(pcc, 1)} #dictionary where gene is key for their rank
  return rank_dict

#Obtain dictionary where gene1 is key for dictionary of gene2:pcc, and vice versa
master_dict = {}
for line in open(path + filename,'r'):
  gene1, gene2, r = line.rstrip().split('\t')
  master_dict.setdefault(gene1,{})
  master_dict.setdefault(gene2,{})
  master_dict[gene1].update({gene2:r})
  master_dict[gene2].update({gene1:r})
for i in master_dict: #replaces gene:pcc dictionary with gene:rank dictionary
  master_dict[i] = rank(master_dict[i])

#Create HRR file
output_file = 'ARATH-matrix-HRR.txt' #replace with own file
v = open(path + output_file,'w')
for line in open(path + filename,'r'):
  gene1, gene2, r = line.rstrip().split('\t')
  rank = str(max(master_dict[gene1][gene2],master_dict[gene2][gene1])) #calculates HRR
  v.write('\t'.join([gene1, gene2, r, rank]) + '\n')
v.close()
print('HRR File has been created') #tells user that HRR file is done
