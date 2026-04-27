import os
import argparse
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
    # arg parsing: no longer asking for user input

    parser = argparse.ArgumentParser(description="SeqSorcerer: Automated RNA-seq Pipeline")
    
    parser.add_argument('--fastq-dir', required=True, help='Internal container path to FASTQ files')
    parser.add_argument('--reference', required=True, help='Internal container path to .fna file')
    parser.add_argument('--gtf', required=True, help='Internal container path to .gtf file')
    parser.add_argument('--outdir', required=True, help='Internal container path for output')
    
    args = parser.parse_args()

    print("\n" + "="*60)
    print("Hello! Welcome to the SeqSorcerer!")
    print("Initializing automated RNA-seq pipeline...")
    print("="*60 + "\n")

    # assign paths from arguments. 
    # these match what .sh script sends to docker
    folder_path = args.fastq_dir
    fasta_location = args.reference
    gtf_location = args.gtf
    output_dir = args.outdir
    
    # Print the versions of each tool
    print("Checking tool versions:")
    for tool_name, command in define_tools().items():
        version_info = check_tool_version(tool_name, command)
        if "Error:" in version_info:
            print(f"{tool_name}: {version_info}")
        else:
            print(f"{tool_name}: {version_info}")

    # Data Organization                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    trimmed_folder_path = os.path.join(output_dir, "trimmed_folder")
    os.makedirs(trimmed_folder_path, exist_ok=True)
    print(f"\n[INFO] Results will be stored in: {output_dir}")
        
    # Execute the Pipeline
    # Step 1: Trimming
    print("\n[STEP 1/4] Trimming raw reads...")
    fastqc_report_out_list = trim_and_fastqc(folder_path, trimmed_folder_path)
    print("Done.")

    # Step 2: Reference Genome Indexing
    print("\n[STEP 2/4] Verifying reference genome index...")
    genome_location_path = os.path.join(output_dir, "aligned_genome")
    os.makedirs(genome_location_path, exist_ok=True)
    
    # Passing fasta_location from argparse
    build_reference_genome(fasta_location, genome_location_path)
    print("Done.")

    # Step 3: Alignment
    print("\n[STEP 3/4] Aligning reads to reference...")
    alignment_folder_path = os.path.join(output_dir, "aligned_folder_bamfiles")
    os.makedirs(alignment_folder_path, exist_ok=True)
    
    automated_alignment(trimmed_folder_path, alignment_folder_path, genome_location_path)
    print("Done.")

    # Step 4: Feature Counts
    print("\n[STEP 4/4] Quantifying gene counts...")
    counts_folder_path = os.path.join(output_dir, "counts_folder")
    os.makedirs(counts_folder_path, exist_ok=True)
    
    run_feature_counts(gtf_location, alignment_folder_path, counts_folder_path)
    
    print("\n" + "="*60)
    print("SUCCESS: Pipeline complete.")
    print(f"Output available in: {output_dir}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()