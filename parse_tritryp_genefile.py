#!/usr/bin/env python
#-*- encoding: utf-8 -*-
"""
TriTrypDB gene file parser
Keith Hughitt <khughitt@umd.edu>

Processes a TriTrypDB gene file and generates several new files, each
containing a different type of information.

The files currently generated include:

    1. <xxx>_gene_list.csv
    1. <xxx>_gene_lengths.csv
    3. <xxx>_go_terms.csv

Examples
--------
./parse_tritryp_genefile.py TriTrypDB-4.2_TcruziEsmeraldo-LikeGene.txt output/

"""
import os
import re
import sys
import csv
import datetime
from operator import itemgetter

def main():
    """Main"""
    # input and outpfile filepaths
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    parts = re.match(r"TriTrypDB-(?P<version>\d\.\d)_(?P<species>\w+)",
                     os.path.basename(input_file))
    species = parts.groupdict()['species']
    version = parts.groupdict()['version']

    filename = '%s_%s_%%s.csv' % (species, version)
    output_file = os.path.join(output_dir, filename)

    # Parse TriTrypDB gene file
    gene_rows = []
    length_rows = []
    go_rows = []

    for line in open(input_file).readlines():
        # Gene ID
        if line.startswith("Gene ID"):
            gene_id = line.split(": ").pop().strip()
            go_terms = []

        # Chromosome number
        elif line.startswith("Chromosome"):
            if (line.startswith("Chromosome: Not Assigned")):
                chromosome = None
            else:
                chromosome = int(line.split(':').pop().strip())

        # Genomic Location
        elif line.startswith("Genomic Location"):
            match = re.search('([\d,]*) - ([\d,]*) \(([-+])\)', line).groups()
            start = int(match[0].replace(",", ""))
            stop = int(match[1].replace(",", ""))
            strand = match[2]

        # Gene Type
        elif line.startswith("Gene Type"):
            gene_type = line.split(":").pop().strip()

        # Product Description
        elif line.startswith("Product Description"):
            description = line.split(":").pop().strip()

        # Transcript length
        elif line.startswith("Transcript Length:"):
            gene_length = int(line.split(':').pop().strip())

        # Gene Ontology terms
        elif line.startswith("GO:"):
            #go_terms = line.split('\t')[0:5]
            go_rows.append([gene_id] + line.split('\t')[0:5])

        # End of gene description
        elif line.startswith("---"):
            # skip gene if not assigned to a chromosome
            if chromosome is None:
                continue
            gene_rows.append([gene_id, chromosome, start, stop, strand,
                              gene_type, gene_length, description])
            length_rows.append([gene_id, gene_length])

    # Sort gene info table by genomic location
    gene_rows = sorted(gene_rows, key=itemgetter(1,2))

    # Write output files
    write_file(output_file % 'genes', input_file, species,
               ["gene_id", "chromosome", "start", "stop", "strand", "type",
                "transcript_length", "description"], gene_rows)

    write_file(output_file % 'gene_lengths', input_file, species,
               ["gene_id", "transcript_length"],
               length_rows)

    write_file(output_file % 'go_terms', input_file, species,
               ["gene_id", "go_id", "ontology", "go_term_name",
                "source", "evidence_code"],
               go_rows)

    # Gene ontology information
    print("Finished! Output saved to %s" % output_dir)

def write_file(filepath, input_file, species, header, rows):
    """Writes gene info to file"""
    timestamp = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    with open(filepath, 'w') as csvfile:
        csvfile.write('#\n')
        csvfile.write('# TriTrypDB GO terms: %s\n' % species)
        csvfile.write('# Generated from %s on %s\n' % (os.path.basename(input_file),
                                                       timestamp))
        csvfile.write('#\n')
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    main()
