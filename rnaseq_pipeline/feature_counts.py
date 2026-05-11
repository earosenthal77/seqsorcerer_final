# import packages
import subprocess
import os

def run_feature_counts(gtf_file, input_folder, output_folder):
    """
    Quantifies gene-level read counts from aligned BAM files.

    Assigns aligned reads or fragments to annotated genes using the provided GTF file.
    Outputs count files for downstream differential expression analysis.
    """
    # iterate through aligned BAM files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.bam'):
            # extract sample name by removing .bam extension
            sample_name = filename.split('.bam')[0]

            # construct full input and output file paths
            bam_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{sample_name}_counts.txt")
               
            # build command for featureCounts
            # -a specifies the annotation file, -o specifies the output count file
            # -s 2 indicates reverse-stranded reads, -p indicates paired-end reads
            command = [
                'featureCounts', '-a', gtf_file, '-o', output_file,
                '-T', '2', '-s', '2', '-Q', '0', '-t', 'gene', '-g', 'gene_id',
                '--minOverlap', '1', '--fracOverlap', '0', '--fracOverlapFeature', '0',
                '-p', '-C', bam_file
            ]

            # execute command and display output
            print(f"Running featureCounts for {sample_name}...")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               
            # capture stdout and stderr
            stdout, stderr = process.communicate()