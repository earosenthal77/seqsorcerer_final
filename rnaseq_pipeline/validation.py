import os
import glob
import sys
from tqdm import tqdm

def validate_inputs(fastq_dir, reference, gtf, outdir):
    """
    Validates all user-provided paths before the pipeline starts.
    Returns True if all checks pass, otherwise exits with a plain-English error.
    """
    print("--- Starting Input Validation ---")

    # 1. Check if the FASTQ directory exists inside the container
    if not os.path.isdir(fastq_dir):
        print(f"ERROR: The directory '{fastq_dir}' was not found. "
              "Did you forget to mount it with the --mount flag?")
        sys.exit(1)

    # 2. Check for actual FASTQ files using glob
    # We use tqdm here to show the user we are scanning the folder
    print(f"Scanning {fastq_dir} for sequencing files...")
    fastq_files = []
    extensions = ['*.fastq', '*.fastq.gz', '*.fq', '*.fq.gz']
    
    for ext in extensions:
        fastq_files.extend(glob.glob(os.path.join(fastq_dir, ext)))

    if not fastq_files:
        print(f"ERROR: No .fastq or .fq files found in {fastq_dir}.")
        sys.exit(1)
    else:
        print(f"SUCCESS: Found {len(fastq_files)} files to process.")

    # 3. Validate Reference Genome and GTF
    for label, path in {"Reference Genome": reference, "GTF Annotation": gtf}.items():
        if not os.path.isfile(path):
            print(f"ERROR: {label} file not found at '{path}'.")
            sys.exit(1)
        print(f"SUCCESS: {label} found.")

    # 4. Validate Output Directory and Permissions
    if not os.path.exists(outdir):
        # Try to create it if it doesn't exist
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