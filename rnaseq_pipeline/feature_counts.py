import subprocess
import os

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