import os
import subprocess
import glob
import tqdm

def check_tool_version(tool_name, command):
    # Run the command to get tool version
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    # Decode stdout and stderr
    stdout_str = result.stdout.decode('utf-8').strip()
    stderr_str = result.stderr.decode('utf-8').strip()
    
    if result.returncode == 0:
        return stdout_str
    else:
        return f"Error: {stderr_str}"

# Define tools and their corresponding commands to check versions
tools = {
    "hisat2": "hisat2 --version",
    "trim_galore": "trim_galore --version",
    "featureCounts": "featureCounts -v"
}

# Print the versions of each tool
print("Checking tool versions:")
for tool_name, command in tools.items():
    version_info = check_tool_version(tool_name, command)
    if "Error:" in version_info:
        print(f"{tool_name}: {version_info}")
    else:
        print(f"{tool_name}: {version_info}")

#check and print packages

def trim_and_fastqc(folder_path, output_dir):
    # Find all R1 and R2 files in the folder
    r1_files = glob.glob(os.path.join(folder_path, '*_R1_001.fastq.gz'))
    r2_files = glob.glob(os.path.join(folder_path, '*_R2_001.fastq.gz'))

    # Sort the files to ensure they are in the same order for pairing
    r1_files.sort()
    r2_files.sort()

    # Check if the number of R1 and R2 files match
    if len(r1_files) != len(r2_files):
        print("Error: Number of R1 and R2 files do not match.")
        return

    # List to store fastqc_report_out paths
    fastqc_report_out_list = []

    # Iterate over each pair of R1 and R2 files
    for r1, r2 in zip(r1_files, r2_files):
        # Define output file names for trim_galore
            # Define output file names for trim_galore
        base_name = os.path.basename(r1).replace('_R1_001.fastq.gz', '')
        trimmed_r1_out = os.path.join(output_dir, f"{base_name}_R1_trimmed.fastq.gz")
        trimmed_r2_out = os.path.join(output_dir, f"{base_name}_R2_trimmed.fastq.gz")
        fastqc_report_out = os.path.join(output_dir, f"{base_name}_Fastqc_Report")
        fastqc_report_out_list.append(fastqc_report_out)

        # Run trim_galore
        trim_cmd = f"trim_galore --fastqc --paired --length 20 --clip_R2 15 --three_prime_clip_R1 15 -o {fastqc_report_out} {r1} {r2}"
        subprocess.run(trim_cmd, shell=True, check=True)

    return fastqc_report_out_list

def build_reference_genome(fasta_location, genome_location):
    # Construct the command to build the reference genome
    build_cmd = f"hisat2-build --large-index -p 16 {fasta_location} {genome_location}/genome_index"
    subprocess.run(build_cmd, shell=True, check=True)

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



def automated_alignment(input_folder, output_folder, genome_location):
    # Iterate through files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('_R1_001_val_1.fq.gz'):
            # Extract sample name
            sample_name = filename.split('_R1_001_val_1.fq.gz')[0]

            # Check if corresponding R2 file exists
            r2_filename = sample_name + '_R2_001_val_2.fq.gz'
            if os.path.exists(os.path.join(input_folder, r2_filename)):
                # Build command
                command = f'hisat2 -t --rna-strandness RF --summary-file {output_folder}{sample_name}.txt -p 24 -x {genome_location_path}/genome_index -1 {input_folder}{filename} -2 {input_folder}{r2_filename} | samtools view -@ 24 -Shu - | samtools sort -@ 24 -n -o {output_folder}{sample_name}.bam'

                # Execute command and display output
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in process.stdout:
                    print(line.decode().strip())


def run_feature_counts(gtf_file, input_folder, output_folder):
    # Iterate through files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.bam'):
            # Extract sample name
            sample_name = filename.split('.bam')[0]  # Get the part before '.bam'

            # Construct full paths
            bam_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{sample_name}_counts.txt")
               
            # Build command for featureCounts
            command = [
                'featureCounts', '-a', gtf_file, '-o', output_file,
                '-T', '2', '-s', '2', '-Q', '0', '-t', 'gene', '-g', 'gene_id',
                '--minOverlap', '1', '--fracOverlap', '0', '--fracOverlapFeature', '0',
                '-p', '-C', bam_file
            ]

            # Execute command and display output
            print(f"Running featureCounts for {sample_name}...")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               
            # Capture stdout and stderr
            stdout, stderr = process.communicate()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
def rna_seq_pipeline():
    print("Hello, welcome to the SeqSorcerer! This is an automated RNA seq pipeline that will take your raw reads and output raw counts files.")
    
    # Prompt for user input
    #folder_path = input("Enter the folder path containing your data: ").strip()
    #output_dir = input("Enter the desired output directory: ").strip()
    folder_path="/Volumes/CaChannel/240617ZebraFinchEmbryo/Lagging"
    output_dir="/Volumes/CaChannel/240617ZebraFinchEmbryo/output_forFullAuto"
    
    # Define trimmed folder path
    trimmed_folder_path = os.path.join(output_dir, "trimmed_folder")
    print(f"Trimmed folder path defined as: {trimmed_folder_path}")
    
    # Create the trimmed folder if it doesn't exist
    print(f"Creating trimmed folder at: {trimmed_folder_path}")
    os.makedirs(trimmed_folder_path, exist_ok=True)
    print(f"Trimmed folder created or already exists at: {trimmed_folder_path}")

    # Continue with the rest of your pipeline
    #gtf_location = input("Enter the location of your .gtf or .gcf file: ").strip()
    #fasta_location = input("Enter the location of your .fna file: ").strip()
    gtf_location = "/Users/miseq/Desktop/24061Zebradata/GCF_003957565.2/genomic.gtf"
    fasta_location = "/Users/miseq/Desktop/24061Zebradata/GCF_003957565.2/GCF_003957565.2_bTaeGut1.4.pri_genomic.fna"

    print("Building your reference genome!")
    genome_location_path = os.path.join(output_dir, "aligned_genome")
    os.makedirs(genome_location_path, exist_ok=True)
    #build_reference_genome(fasta_location, genome_location_path)
    print("Reference genome is built.")

    print("Now trimming your raw reads.")
    #trim_and_fastqc(folder_path, trimmed_folder_path)
    print("Reads are trimmed.")

    alignment_folder_path = os.path.join(output_dir, "aligned_folder_bamfiles")
    os.makedirs(alignment_folder_path, exist_ok=True)
    print(trimmed_folder_path)
    print(fastqc_report_out_list)
    print(alignment_folder_path)
    print(genome_location_path)
    for fastqc_report_out in fastqc_report_out_list:
        automated_alignment(fastqc_report_out, alignment_folder_path, genome_location_path)
    
    print("Reads are aligned.")

    counts_folder_path = os.path.join(output_dir, "counts_folder")
    os.makedirs(counts_folder_path, exist_ok=True)
    print(counts_folder_path)
    print(gtf_location)
    print(alignment_folder_path)
    print(counts_folder_path)
    run_feature_counts(gtf_location, alignment_folder_path, counts_folder_path)
    print("Pipeline is complete.")

rna_seq_pipeline()