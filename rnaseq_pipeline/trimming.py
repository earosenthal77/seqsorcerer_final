# import statements
import glob
import os
import subprocess

def trim_and_fastqc(folder_path, output_dir):
    """
    Removes artificial adapter sequences and low-quality bases from raw FASTQ files.
    Returns trimmed FASTQ files.
    """
    # find all R1 and R2 files in the raw reads folder
    r1_files = glob.glob(os.path.join(folder_path, '*_R1_001.fastq.gz'))
    r2_files = glob.glob(os.path.join(folder_path, '*_R2_001.fastq.gz'))

    # sort the files so they are in the same order for pairing
    r1_files.sort()
    r2_files.sort()

    # check if the number of R1 and R2 files match
    if len(r1_files) != len(r2_files):
        print("Error: Number of R1 and R2 files do not match.")
        return

    # list to store fastqc_report_out paths
    fastqc_report_out_list = []

    # iterate over each pair of R1 and R2 files
    for r1, r2 in zip(r1_files, r2_files):
        # define output file names for trim_galore
        base_name = os.path.basename(r1).replace('_R1_001.fastq.gz', '')
        fastqc_report_out = os.path.join(output_dir, f"{base_name}_Fastqc_Report")

        # check if trimmed files already exist
        check_file = os.path.join(fastqc_report_out, f"{base_name}_R1_001_val_1.fq.gz")

        # if the trimmed file already exists, skip trimming for that pair
        if os.path.exists(check_file):
            print(f"SKIP: Trimmed files for {base_name} already exists.")
            fastqc_report_out_list.append(fastqc_report_out)
            continue # move on to next pair of files

        print(f"Trimming sample {base_name}...")
        fastqc_report_out_list.append(fastqc_report_out)

        # run trim_galore command
        trim_cmd = f"trim_galore --fastqc --paired --length 20 --clip_R2 15 --three_prime_clip_R1 15 -o {fastqc_report_out} {r1} {r2}"
        subprocess.run(trim_cmd, shell=True, check=True)

    return fastqc_report_out_list