import subprocess
import os

def build_reference_genome(fasta_location, genome_location):

    index_base = os.path.join(genome_location, "genome_index")
    # Construct the command to build the reference genome
    build_cmd = f"hisat2-build --large-index -p 16 {fasta_location} {index_base}"
    subprocess.run(build_cmd, shell=True, check=True)
    return

def get_fasta_header(fasta_location):
    with open(fasta_location, 'r') as fasta_file:
        first_line = fasta_file.readline().strip()
        if first_line.startswith('>'):
            return first_line[1:]  # Remove the '>' character
        else:
            raise ValueError("Invalid FASTA file format. First line should start with '>'")

def get_gtf_header(gtf_location):
    with open(gtf_location, 'r') as gtf_file:
        for line in gtf_file:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                if len(fields) >= 9:
                    return fields[0]  # Return the first column (NC_054371.1 in this case)
                else:
                    raise ValueError("Invalid GTF file format. Expected at least 9 columns.")



def fastagffcheck(fasta_location, gtf_location):
    # Read the FASTA header
    with open(fasta_location, 'r') as fasta_file:
        fasta_header = fasta_file.readline().strip()
        fasta_identifier = fasta_header.split()[0][1:]  # Get the first part of the header without '>'

    # Read the GTF header
    with open(gtf_location, 'r') as gtf_file:
        for line in gtf_file:
            if line.startswith('##sequence-region'):
                gtf_identifier = line.split()[1]  # Extract identifier from specific line
                break

