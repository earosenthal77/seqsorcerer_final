# import packages
import subprocess
import os

def build_reference_genome(fasta_location, genome_location):
    """
    Builds a searchable data structure from the reference genome FASTA file.
    Outputs HISAT2 index files with the prefix 'genome_index' unless they already exist.
    """
    # location for reference genome index
    index_base = os.path.join(genome_location, "genome_index")

    # check to see if the index already exists
    large_index = index_base + ".1.ht2l"
    small_index = index_base + ".1.ht2"
    
    # if the indexed reference genome is found, do NOT remake it
    if os.path.exists(large_index) or os.path.exists(small_index):
        print(f"SKIP: Genome index already found at {index_base}. Moving to next step.")
        return
    
    print("Building reference genome index...")
    # construct the command to build the reference genome
    build_cmd = f"hisat2-build --large-index -p 16 {fasta_location} {index_base}"
    subprocess.run(build_cmd, shell=True, check=True)
    return

def get_fasta_header(fasta_location):
    """
    Reads in the first header line of a FASTA file and extracts first sequence identifier.
    The '>' character is removed so the FASTA sequence ID can be directly compared to GTF IDs.
    """
    with open(fasta_location, 'r') as fasta_file:
        first_line = fasta_file.readline().strip()
        if first_line.startswith('>'):
            return first_line[1:]  # remove the '>' character
        else:
            # FASTA file validation
            raise ValueError("Invalid FASTA file format. First line should start with '>'")

def get_gtf_header(gtf_location):
    """
    Reads the first non-comment line of a GTF file and extracts sequence identifier from the first column.
    Used to check whether the FASTA and GTF files use compatible chromosome or scaffold naming conventions.
    """
    with open(gtf_location, 'r') as gtf_file:
        for line in gtf_file:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                if len(fields) >= 9:
                    return fields[0]  # Return the first column (NC_054371.1 in this case)
                else:
                    raise ValueError("Invalid GTF file format. Expected at least 9 columns.")

def fastagffcheck(fasta_location, gtf_location):
    """
    Checks both FASTA and GTF files use compatible sequence identifiers.
    Compares the first FASTA sequence ID with an ID found in the GTF file.
    Helps detect mismatches between the reference genome and annotation file before alignment and read counting.
    """
    fasta_identifier = get_fasta_header(fasta_location).split()[0] # get the first part of the header without '>'
    gtf_identifier = get_gtf_header(gtf_location) # extract identifier from specific line

    if fasta_identifier == gtf_identifier:
        print("FASTA and GTF sequence identifiers match")
    else:
        raise ValueError(
            f"FASTA and GTF identifiers do not match.\n"
            f"FASTA identifier: {fasta_identifier}\n"
            f"GTF identifier: {gtf_identifier}\n"
            "Check that the genome FASTA and annotation GTF come from the same reference assembly."
        )

