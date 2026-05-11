# import packages
import os
import glob
import sys
from tqdm import tqdm

def validate_inputs(fastq_dir, reference, gtf, outdir):
    """
    Validates all user-provided paths before the pipeline starts.
    Returns True if all checks pass, otherwise exits with an error.
    """
    print("--- Starting Input Validation ---")

    # 1. check if the FASTQ directory exists inside the container
    if not os.path.isdir(fastq_dir):
        print(f"ERROR: The directory '{fastq_dir}' was not found. "
              "Did you forget to mount it with the --mount flag?")
        sys.exit(1)

    # 2. check for actual FASTQ files using glob
    # tqdm to show the user the folder is being scanned
    print(f"Scanning {fastq_dir} for sequencing files...")
    fastq_files = []
    # define common FASTQ extensions to ensure compatability with varied naming conventions
    extensions = ['*.fastq', '*.fastq.gz', '*.fq', '*.fq.gz']
    
    for ext in extensions:
        fastq_files.extend(glob.glob(os.path.join(fastq_dir, ext)))

    if not fastq_files:
        print(f"ERROR: No .fastq or .fq files found in {fastq_dir}.")
        sys.exit(1)
    else:
        print(f"SUCCESS: Found {len(fastq_files)} files to process.")

    # 3. validate reference genome and GTF
    for label, path in {"Reference Genome": reference, "GTF Annotation": gtf}.items():
        if not os.path.isfile(path):
            print(f"ERROR: {label} file not found at '{path}'.")
            sys.exit(1)
        print(f"SUCCESS: {label} found.")

    # 4. validate output directory and permissions
    if not os.path.exists(outdir):
        # try to create it if it doesn't exist
        try:
            os.makedirs(outdir, exist_ok=True)
            print(f"SUCCESS: Created output directory at {outdir}.")
        except Exception as e:
            print(f"ERROR: Could not create output directory. {e}")
            sys.exit(1)
            
    if not os.access(outdir, os.W_OK):
        print(f"ERROR: Output directory '{outdir}' is not writable. "
              "Check your mount permissions.")
        sys.exit(1)

    print("--- All checks passed! Starting pipeline. ---\n")
    return True