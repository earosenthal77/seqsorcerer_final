import os
import subprocess
import glob
import tqdm
from importlib import reload 

#import from files: 
from rnaseq_pipeline.check_tool import check_tool_version, define_tools
from rnaseq_pipeline.trimming import trim_and_fastqc
from rnaseq_pipeline.reference_genome import build_reference_genome, get_fasta_header, get_gtf_header, fastagffcheck
from rnaseq_pipeline.alignment import automated_alignment
from rnaseq_pipeline.feature_counts import run_feature_counts

def main():

    print("Hello, welcome to the SeqSorcerer! This is an automated RNA seq pipeline that will take your raw reads and output raw counts files.")

    # Print the versions of each tool
    print("Checking tool versions:")
    for tool_name, command in define_tools().items():
        version_info = check_tool_version(tool_name, command)
        if "Error:" in version_info:
            print(f"{tool_name}: {version_info}")
        else:
            print(f"{tool_name}: {version_info}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

    # Prompt for user input
    #folder_path="/Volumes/CaChannel/240617ZebraFinchEmbryo/Lagging"
    folder_path = "./data/testing"
    #output_dir="/Volumes/CaChannel/240617ZebraFinchEmbryo/output_forFullAuto"
    output_dir="./data/output"
        
    # Define trimmed folder path
    trimmed_folder_path = os.path.join(output_dir, "trimmed_folder")
    print(f"Trimmed folder path defined as: {trimmed_folder_path}")
    # Create the trimmed folder if it doesn't exist
    print(f"Creating trimmed folder at: {trimmed_folder_path}")
    os.makedirs(trimmed_folder_path, exist_ok=True)
    print(f"Trimmed folder created or already exists at: {trimmed_folder_path}")

    #trim the raw reads
    print("Now trimming your raw reads.")
    fastqc_report_out_list = trim_and_fastqc(folder_path, trimmed_folder_path)
    print("Reads are trimmed.")

    # Continue with the rest of your pipeline
    #gtf_location = "/Users/miseq/Desktop/24061Zebradata/GCF_003957565.2/genomic.gtf"
    #fasta_location = "/Users/miseq/Desktop/24061Zebradata/GCF_003957565.2/GCF_003957565.2_bTaeGut1.4.pri_genomic.fna"

    print("Building your reference genome!")
    genome_location_path = os.path.join(output_dir, "aligned_genome")
    if not os.path.exists(genome_location_path):
        os.makedirs(genome_location_path, exist_ok=True)
        build_reference_genome(fasta_location, genome_location_path)
    print("Reference genome is built.")

    alignment_folder_path = os.path.join(output_dir, "aligned_folder_bamfiles")
    os.makedirs(alignment_folder_path, exist_ok=True)
    print(trimmed_folder_path)
    print(fastqc_report_out_list)
    print(alignment_folder_path)
    print(genome_location_path)
    automated_alignment(trimmed_folder_path, alignment_folder_path, genome_location_path)
        
    print("Reads are aligned.")

    counts_folder_path = os.path.join(output_dir, "counts_folder")
    os.makedirs(counts_folder_path, exist_ok=True)
    print(counts_folder_path)
    print(gtf_location)
    print(alignment_folder_path)
    print(counts_folder_path)
    run_feature_counts(gtf_location, alignment_folder_path, counts_folder_path)
    print("Pipeline is complete.")

    return