import os 
import subprocess

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
                command = f'hisat2 -t --rna-strandness RF --summary-file {output_folder}{sample_name}.txt -p 24 -x {genome_location}/genome_index -1 os.path.join(input_folder, filename) -2 {input_folder}{r2_filename} | samtools view -@ 24 -Shu - | samtools sort -@ 24 -n -o os.path.join(output_folder, f"{sample_name}.bam")'

                # Execute command and display output
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in process.stdout:
                    print(line.decode().strip())