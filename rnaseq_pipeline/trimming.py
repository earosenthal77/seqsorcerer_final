import glob
import os
import subprocess

def trim_and_fastqc(folder_path, output_dir):
    # Find all R1 and R2 files in the folder
    r1_files = glob.glob(os.path.join(folder_path, '*_R1_first100.fastq'))
    r2_files = glob.glob(os.path.join(folder_path, '*_R2_first100.fastq'))

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
        fastqc_report_out = os.path.join(output_dir, f"{base_name}_Fastqc_Report")

        # Check if trimmed files already exist
        check_file = os.path.join(fastqc_report_out, f"{base_name}_R1_001_val_1.fq.gz")

        if os.path.exists(check_file):
            print(f"SKIP: Trimmed files for {base_name} already exists.")
            fastqc_report_out_list.append(fastqc_report_out)
            continue # move on to next pair of files

        print(f"Trimming sample {base_name}...")
        fastqc_report_out_list.append(fastqc_report_out)

        # Run trim_galore
        trim_cmd = f"trim_galore --fastqc --paired --length 20 --clip_R2 15 --three_prime_clip_R1 15 -o {fastqc_report_out} {r1} {r2}"
        subprocess.run(trim_cmd, shell=True, check=True)

    return fastqc_report_out_list