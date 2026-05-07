import os 
import subprocess

def automated_alignment(input_folder, output_folder, genome_location):
    
    print(f"--- DEBUG: Starting Alignment Search in {input_folder} ---")
    
    found_any_file = False


    # Iterate through files in the input folder
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            found_any_file = True

            #print files found: 
            print(f"Checking file: {filename}")

            #look for the R1 trimmed file: 
            if '_R1' in filename and filename.endswith('_val_1.fq'):
                print(f"MATCH FOUND: {filename} looks like a trimmed R1 file.")

                #get the r1 path: 
                r1_path = os.path.join(root, filename)
                #edit the r1 path to get the r2 path: 
                r2_filename = filename.replace('_val_1', '_val_2').replace('_R1', '_R2')
                r2_path = os.path.join(root, r2_filename)

                # Extract sample name
                sample_name = filename.split('_R1_first100_001_val_1.fq')[0]

                if os.path.exists(r2_path):

                    #create file paths for use in command: 
                    summary_file = os.path.join(output_folder, f"{sample_name}_summary.txt")
                    bam_output = os.path.join(output_folder, f"{sample_name}.bam")
                    index_prefix = os.path.join(genome_location, "genome_index")

                    # Build command
                    command = (
                        f'hisat2 -t --rna-strandness RF --summary-file {summary_file}'
                        f' -p 24 -x {index_prefix} -1 {r1_path} -2 {r2_path} |' 
                        f' samtools view -@ 24 -Shu - | samtools sort -@ 24 -o {bam_output}' 
                    )
                    print(f"RUNNING COMMAND: {command}")
                    # Execute command and display output
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in process.stdout:
                        print(line.decode().strip())
                    else: 
                        print(f"ERROR: Found R1 but R2 is missing at: {r2_path}")
                else:
                    pass

                if not found_any_file:
                    print("ERROR: os.walk found ZERO files in the input folder. Check your mount paths!")

                    #make sure alignment finishes before starting feature counts
                    process.wait() 
                    if process.returncode != 0:
                        print(f"Alignment failed for {sample_name} with exit code {process.returncode}")
                    else:
                        print(f"Alignment finished for {sample_name}")