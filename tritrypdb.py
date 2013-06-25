"""
TriTrypDB gene information table parser
Author: Keith Hughitt <khughitt@umd.edu>

An example input file is the T. brucei Lister427 gene information table
available at:
http://tritrypdb.org/common/downloads/Current_Release/TbruceiLister427/txt/data/TriTrypDB-5.0_TbruceiLister427Gene.txt

See Also
--------
1. http://tritrypdb.org/tritrypdb/
2. http://www.github.com/khughitt/tritrypdb
"""
import re
from pandas import DataFrame
from operator import itemgetter

def parse_gene_info_table(filepath, verbose=False):
    """
    TriTrypDB gene information table parser

    Parameters
    ----------
    filepath : str
        Location of TriTrypDB gene information table to use input.
    verbose : bool
        Whether or not to display progress information during parsing.
    """
    gene_rows = []

    # Regular expresion to extract location info
    location_regex = '([\d,]*) - ([\d,]*) \(([-+])\)'

    i = 0
    for line in open(filepath).readlines():
        # Gene ID
        if line.startswith("Gene ID"):
            gene_id = line.split(": ").pop().strip()

            i += 1
            if verbose:
                print("Processing gene %d: %s" % (i, gene_id))

        # Chromosome number
        elif line.startswith("Chromosome"):
            if (line.startswith("Chromosome: Not Assigned")):
                chromosome = None
            else:
                chromosome = int(line.split(':').pop().strip())

        # Genomic Location
        elif line.startswith("Genomic Location"):
            match = re.search(location_regex, line).groups()
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
            transcript_length = int(line.split(':').pop().strip())

        # CDS length
        elif line.startswith("CDS Length"):
            val = line.split(':').pop().strip()
            if val == "null":
                cds_length = None
            else:
                cds_length = int(val)

        # Pseudogene?
        elif line.startswith("Is Pseudo:"):
            is_pseudo = 1 if (line.split(':').pop().strip() == "Yes") else 0

        # End of gene description
        elif line.startswith("---"):
            # skip gene if not assigned to a chromosome
            if chromosome is None:
                continue
            gene_rows.append([gene_id, chromosome, start, stop, strand,
                              gene_type, transcript_length, cds_length,
                              is_pseudo, description])

    # Sort gene info table by genomic location
    gene_rows = sorted(gene_rows, key=itemgetter(1,2))

    # convert to pandas dataframe and return
    colnames = ["gene_id", "chromosome", "start", "stop", "strand", "type",
                "transcript_length", "cds_length",
                "pseudogene", "description"]

    return DataFrame(gene_rows, columns=colnames)

def parse_gene_go_terms(filepath, verbose=False):
    """
    TriTrypDB gene information table GO term parser

    Parameters
    ----------
    filepath : str
        Location of TriTrypDB gene information table to use input.
    verbose : bool
        Whether or not to display progress information during parsing.
    """
    go_rows = []

    i = 0
    for line in open(filepath).readlines():
        # Gene ID
        if line.startswith("Gene ID"):
            gene_id = line.split(": ").pop().strip()

            i += 1
            if verbose:
                print("Processing gene %d: %s" % (i, gene_id))

        # Gene Ontology terms
        elif line.startswith("GO:"):
            go_rows.append([gene_id] + line.split('\t')[0:5])

    # Convert to dataframe
    colnames = ["gene_id", "go_id", "ontology", "go_term_name",
                "source", "evidence_code"]

    return DataFrame(go_rows, columns=colnames)

