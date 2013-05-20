#!/usr/bin/env python
#-*- encoding: utf-8 -*-
"""
Tryp2GO
Keith Hughitt <khughitt@umd.edu>

2012/12/09

Processes a TriTrypDB file containing Trypanosome gene ontology (GO) terms and
return a new table mapping gene id's to GO terms.

"""
import os
import sys
import csv
import datetime

# input and outpfile filepaths
input_file = "../data/TriTrypDB-4.2_TcruziEsmeraldo-LikeGene.txt"
output_file = 'output/TcruziEsmeraldo_GOTerms_4.2.tsv'

# Parse TriTrypDB GO terms
current_id = None
current_len = None
mapping = []

for line in open(input_file).readlines():
    if line.startswith("Gene ID"):
        current_id = line.split(": ").pop().strip()
    elif line.startswith("Transcript Length:"):
        current_len = int(line.split(':').pop().strip())
    elif line.startswith("GO:"):
        mapping.append([current_id, current_len] + line.split('\t')[0:5])

# Write output to a new file
timestamp = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

with open(output_file, 'w') as csvfile:
    csvfile.write('#\n')
    csvfile.write('# TriTrypDB gene ID to GO term mapping\n')
    csvfile.write('# Generated from %s on %s\n' % (os.path.basename(input_file),
                                                   timestamp))
    csvfile.write('#\n')
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(["gene_id", "transcript_length", "go_id", "ontology", "go_term_name", 
                     "source", "evidence_code"])
    writer.writerows(mapping)

print("Done! Output saved to %s" % output_file)

