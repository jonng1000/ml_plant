# -*- coding: utf-8 -*-
"""
Created on 290520

@author: weixiong

Takes in a peptide file, primary transcript only, downloaded from
JGI Phytozome. This is the translated amino acid sequences from its
corresponding cds file. Removes decimals from gene IDs and converts
it to a whole number. Since the input file only has primary transcripts,
I can assume that there are not >1 isoform per gene, and the decimal
values are not important (since typically .1 means primary isoform).
Removes * at the end of the sequences since IntroProScan cannot
handle it.
"""

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import single_letter_alphabet

original_file = "Athaliana_447_Araport11.protein_primaryTranscriptOnly.fa"
corrected_file = "ath_aa_processed.fa"

# Set of all genes, to verify that genes are unique
# 27654 genes in this set
gene_set = set()
# Parsing and processing fasta sequences
with open(original_file) as orig, open(corrected_file, 'w') as corrected:
    records = SeqIO.parse(original_file, 'fasta')
    for record in records:
        # Removes decimal values from gene IDs 
        new_id = record.id.split('.')[0]
        record.id = new_id
        # Verifies that genes are unique
        if record.id in gene_set:
            print(record.id, 'exists')
        else:
            gene_set.add(record.id)
        # Removes gene description
        record.description = ''
        # Removes * from end of sequence
        temp = str(record.seq).replace('*', '')
        no_asterisk = Seq(temp, single_letter_alphabet)
        record.seq = no_asterisk
        SeqIO.write(record, corrected, 'fasta')
